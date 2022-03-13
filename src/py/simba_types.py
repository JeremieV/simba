"""
The data types for the Simba interpreter.
Many data types are declared as aliases for the benefit of being able to call isinstance() to determine type (Maybe this is a bad idea).
"""
from re import split
import helpers
from simba_exceptions import UnresolvedSymbolError, ImmutableBindingException, SimbaSyntaxError, SimbaException
import pyrsistent as p

# Atomic Data Types
class Symbol:
    def __init__(self, string):
        split_str = split('/', string)
        if string == '/': self.name = '/'; self.namespace = None
        elif len(split_str) > 2: raise SimbaSyntaxError("A symbol can only have one namespace qualifier.", string, None, None)
        elif len(split_str) == 2:
            if split_str[0] == '' or split_str[1] == '': raise SimbaSyntaxError("None of the two members of the symbol should be empty.", string, None, None)
            self.namespace = split_str[0]
            self.name = split_str[1]
        elif len(split_str) == 1:
            if split_str[0] == '': raise SimbaSyntaxError("A symbol cannot be empty.", string, None, None)
            self.namespace = None
            self.name = split_str[0]
    def __str__(self):
        if self.namespace: return '/'.join([self.namespace, self.name])
        else: return self.name
    def __repr__(self):
        return str(self)
    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, Symbol): return False
        if __o.name == self.name and __o.namespace == self.namespace: return True
        return False

# Number = (int, float)
Environment = dict
class Keyword(str): pass

# Symbolic Data Types

class SymbolicExpression():
    """A symbolic expression contains: symbol, positional arguments, relational arguments"""
    def __init__(self, *args, **kwargs):
        self.positional = []
        self.relational = {**kwargs}
        _skip = False
        for i, e in enumerate(args):
            if _skip: _skip = False; continue
            if not isinstance(e, Keyword):
                self.positional.append(e)
            else:
                self.relational[str(e)] = args[i+1]
                _skip = True

    def append(self, e):
        self.positional.append(e)

    def __repr__(self):
        return '<SymbolicExpression>(' + str(self.positional) + str(self.relational) + ')'

    def __contains__(self, item):
        """This method overrides the Python `in` operator:
        - If `item` is a Keyword, look in the relational arguments
        - else, look in the positional arguments"""
        if isinstance(item, Keyword) or isinstance(item, str):
            return str(item) in self.relational
        else:
            return item in self.positional

    def __getitem__(self, __slice):
        if isinstance(__slice, str):
            return self.relational[__slice]
        else:
            return self.positional[__slice]

    def __eq__(self, __o):
        if not isinstance(__o, SymbolicExpression): return False
        return  len(self) == len(__o) \
            and all(value == __o[i] for i, value in enumerate(self.positional)) \
            and all(key in __o and self[key] == __o[key] for key in self.relational if key != 'meta')

    def __len__(self):
        return len(self.positional) + len(self.relational)

    def __add__(self, sexp):
        if isinstance(sexp, SymbolicExpression):
            self.positional = self.positional + sexp.positional
            self.relational = self.relational | sexp.relational
            return self
        # elif isinstance(sexp, tuple):
        #     self.positional = self.positional + SymbolicExpression(sexp).positional
        #     return self
        else:
            raise SimbaException(f"Tried to concat SymbolicExpression with unsupported type {type(sexp)}", sexp, None, None)

# Collection Data Types

List = p.PList
Vector = p.PVector
Map = p.PMap

class Protocol():
    """This is the protocol type"""

# =====================
#       INTERNAL
# =====================

class Environment():
    """Just like a scheme environment. Contains a mapping of symbols to namespaces and an outer environment.
    An addition that is made to the typical environment"""
    def __init__(self, outer = None, names = None, namespaces = None, referred = None, name = None):
        self.outer = outer
        self.names = {} if names is None else names
        self.namespaces = {} if namespaces is None else namespaces
        self.referred = [] if referred is None else referred
        # the presence of a name indicates that the environment is a namespace
        # as such, `if (env.name)` serves to know if `env` is an `ns`
        self.name = name
        # self.ns_name = ns_name
    def set(self, symbol, value):
        """Change or add a binding. The binding has to be in the local namespace."""
        if symbol.namespace is not None and self.ns_name != symbol.namespace:
            raise SimbaException("Cannot change a binding outside of current namespace.", None, self, self.ns_name)
        env = self.find(symbol)
        if env is None or env is self:
            self.names[symbol.name] = value
        else:
            env.set(symbol, value)
    def find(self, symbol):
        """Looks for a binding, first in current env, and then in outer, and so on. Returns the env where the match is made first."""
        # there is a bug here bc you have to look in the namespaces of the outer envs also
        # print(f"finding {symbol}")
        ns = symbol.namespace
        # if the symbol is namespace-qualified, look for the binding directly in that namespace.
        if ns is not None:
            if self.ns_name == ns:
                return self
            elif ns in self.namespaces:
                return self.namespaces[ns]
            else:
                return self.outer.find(symbol)
        if symbol.name in self.names:
            return self
        # this aims to find the env of a symbol contained in a referred ns
        # however there is a problem because this should allow us to rebind
        # symbols in all referred namespaces, which is not intentional (see `set`)
        # print(self.referred)
        if self.outer is not None:
            return self.outer.find(symbol)
        for n in self.referred:
            if symbol.name in n.names:
                return n
        return None
    def get(self, symbol):
        """Returns the binding if it is in current env or parents."""
        # print(f"getting {symbol}")
        strkey = symbol.name
        # there is a bug here bc you have to look in the namespaces of the outer envs also
        # if symbol.namespace != None: return self.namespaces[strkey].get(symbol)
        if strkey in self.names:
            return self.names[strkey]
        location = self.find(symbol)
        if location is None:
            raise UnresolvedSymbolError(strkey, strkey, self, self.name)
        return location.get(symbol)
    def require_ns(self, ns_name:str, ns):
        self.namespaces[ns_name] = ns
    def include_ns(self, name, ns):
        self.require_ns(name, ns)
        self.referred.append(ns)
        # it's also possible to refer individual names by creating small namespaces

# class Namespace(Environment):
#     """Just like an environment except that it has a dictionary of required and included namespaces."""
#     def __init__(self):
#         self.name = name
#     def set(self, symbol, value):
#         """Change or add a binding. The binding has to be in the current namespace."""
#         if symbol.namespace is not None and symbol.namespace != self.name:
#             raise ImmutableBindingException("Cannot mutate a binding outside of current namespace.")
#         env = self.find(symbol)
#         if env is None or env is self:
#             self.names[symbol.name] = value
#         else:
#             env.set(symbol, value)
#     def find():
#         pass
#     def get():

#     def require_ns(self, ns_name:str, ns):
#         self.namespaces[ns_name] = ns
#     def include_ns(self, name, ns):
#         self.require_ns(name, ns)
#         self.referred.append(ns)