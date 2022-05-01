from re import split
from simba.exceptions import UnresolvedSymbolError, ImmutableBindingException, SimbaSyntaxError, SimbaException
# import pyrsistent as p
from pyrsistent import PMap, PVector, pvector, pmap

class Keyword(str): pass

PersistentVector = PVector

def createVector(args):
    from simba.lang.PersistentList import PersistentList
    t = pvector(args)
    # t.cons = lambda self, x: PersistentList.create(x, *self)
    return t

PersistentVector.create = createVector

PersistentMap = PMap

def createMap(m = None):
    t = pmap(m) if m is not None else pmap()
    return t

PersistentMap.create = createMap


def make_meta_map(m) -> PersistentMap:
    # the m should be evaluated
    if isinstance(m, PersistentMap):
        return m
    elif isinstance(m, Symbol): # should be 'type'
        return PersistentMap.create({Keyword('tag'): m})
    elif isinstance(m, Keyword):
        return PersistentMap.create({m: True})
    # elif isinstance(m, str):
    #     return PersistentMap.create({Keyword('tag'), Symbol(m)})
    else:
        raise SimbaException(f"The type {type(m)} cannot serve as metadata. Only PersistentMap, type, and Keyword are allowed.")

# Atomic Data Types
class Symbol:
    def __init__(self, string):
        # NOTE: much of this logic belongs in the reader
        split_str = split('/', string)
        if string == '/': self.name = '/'; self.namespace = None
        elif len(split_str) > 2: raise SimbaSyntaxError(f"A symbol can only have one namespace qualifier (symbol `{string}`).")
        elif len(split_str) == 2:
            if split_str[0] == '' or split_str[1] == '': raise SimbaSyntaxError("None of the two members of the symbol should be empty.")
            self.namespace = split_str[0]
            self.name = split_str[1]
        elif len(split_str) == 1:
            if split_str[0] == '': raise SimbaSyntaxError("A symbol cannot be empty.")
            self.namespace = None
            self.name = split_str[0]
        self.meta = PersistentMap.create()
        if len(self.name) > 1 and self.name.endswith('.'):
            self.name = self.name[:-1]
    def __str__(self):
        if self.namespace: return '/'.join([self.namespace, self.name])
        else: return self.name
    def __repr__(self):
        return str(self)
    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, Symbol): return False
        if __o.name == self.name and __o.namespace == self.namespace: return True
        return False
    def withMeta(self, m):
        self.meta = self.meta | make_meta_map(m)
        return self

class Unbound: pass

class Var:
    """If a Var is static it means that its value is the same regardless of the thread.
    A dynamic Var can have different values depending on the thread.
    By default Vars are static, as access is faster for static Vars.

    Currently the implementation only supports static Vars.
    """
    def __init__(self, ns, sym:Symbol, root = Unbound):
        self.ns = ns
        self.sym = sym
        # self.dynamic = False
        # self.threadBound = False
        self.root = root
        self.meta = PersistentMap.create({Keyword('name'): sym, Keyword('ns'): ns})
    def get(self):
        return self.deref()
    def set(self, v):
        self.root = v
    def deref(self):
        return self.root
    # isMacro, isPublic ...
    def __repr__(self):
        return f"#'{self.ns.name}/{self.sym.name}"
    # def set_dynamic(self, b = True):
    #     self.dynamic = b
    #     return self
    def withMeta(self, m):
        self.meta = self.meta | make_meta_map(m)
        return self

# Symbolic Data Types

# class SymbolicExpression():
#     """A symbolic expression contains: symbol, positional arguments, relational arguments"""
#     def __init__(self, *args, **kwargs):
#         self.positional = []
#         self.relational = {**kwargs}
#         _skip = False
#         for i, e in enumerate(args):
#             if _skip: _skip = False; continue
#             if not isinstance(e, Keyword):
#                 self.positional.append(e)
#             else:
#                 self.relational[str(e)] = args[i+1]
#                 _skip = True

#     def append(self, e):
#         self.positional.append(e)

#     def __repr__(self):
#         return '<SymbolicExpression>(' + str(self.positional) + str(self.relational) + ')'

#     def __contains__(self, item):
#         """This method overrides the Python `in` operator:
#         - If `item` is a Keyword, look in the relational arguments
#         - else, look in the positional arguments"""
#         if isinstance(item, Keyword) or isinstance(item, str):
#             return str(item) in self.relational
#         else:
#             return item in self.positional

#     def __getitem__(self, __slice):
#         if isinstance(__slice, str):
#             return self.relational[__slice]
#         else:
#             return self.positional[__slice]

#     def __eq__(self, __o):
#         if not isinstance(__o, SymbolicExpression): return False
#         return  len(self) == len(__o) \
#             and all(value == __o[i] for i, value in enumerate(self.positional)) \
#             and all(key in __o and self[key] == __o[key] for key in self.relational if key != 'meta')

#     def __len__(self):
#         return len(self.positional) + len(self.relational)

#     def __add__(self, sexp):
#         if isinstance(sexp, SymbolicExpression):
#             self.positional = self.positional + sexp.positional
#             self.relational = self.relational | sexp.relational
#             return self
#         # elif isinstance(sexp, tuple):
#         #     self.positional = self.positional + SymbolicExpression(sexp).positional
#         #     return self
#         else:
#             raise SimbaException(f"Tried to concat SymbolicExpression with unsupported type {type(sexp)}")

class Protocol():
    """This is the protocol type"""
    pass

class Environment():
    """Corresponds to the scope of a `let` form. Importantly, the bindings created are immutable."""
    def __init__(self, outer, names = None):
        self.outer = outer
        self.names = {} if names is None else names
        self.ns = outer.ns
    def get(self, symbol, deref_var = True):
        """Looks for a binding, first in current env, and then in outer, and so on.
        Return the value bound to the given symbol."""
        n = symbol.name
        # 1. if the symbol is namespace-qualified, look in the appropriate namespace
        if symbol.namespace is not None:
            self.ns.get(symbol, deref_var = deref_var)
        # 2. else look in the local names
        if symbol.name in self.names:
            return self.names[n]
        # 3. if not found, look in outer envs
        else:
            return self.outer.get(symbol, deref_var = deref_var)
        # NB: You only want to look for referred names at the ns level
    def set(self, symbol, val):
        if symbol.namespace: raise SimbaException(f"Illegal definition of the namespaced symbol `{symbol.namespace}/{symbol.name}` in a let statement.")
        self.names[symbol.name] = val

from simba.lang.RT import repl_env

class Namespace():
    """Just like an environment except that it has a dictionary of required and included namespaces.
    A name that equals to the empty string denotes that the env is an empty shell and has to be mutated."""
    def __init__(self, name = "", names = None):
        self.name = name
        self.names = names if names else repl_env.copy()
        self.namespaces = {}
        self.referred = []
        self.ns = self
    def set(self, symbol, value):
        """Change or add a binding. The binding has to be in the current namespace."""
        if symbol.namespace is not None and symbol.namespace != self.name:
            raise ImmutableBindingException(f"Cannot mutate the binding `{symbol}` from the current namespace {self.name}.")
        self.names[symbol.name] = value
    def get(self, symbol, deref_var = True):
        """Looks for a binding in namespace.
        If the binding is namespace-qualified and doesn't exist in that ns, throws an error.
        Else, if the binding doesn't exist, throws an error"""
        n = symbol.name
        ns = symbol.namespace
        # 1. look in external namespaces if the symbol is ns-qualified
        if ns is not None and ns != self.name:
            try:
                # makes sure the binding exists in the external namespace, 
                # otherwise throwing an error is the expected behavior
                if isinstance(v := self.namespaces[ns].names[n], Var) and deref_var:
                    return v.deref()
                else:
                    return r
            except KeyError:
                raise UnresolvedSymbolError(f"\n\tThe symbol `{symbol}` could not be found.\n\tMake sure the namespace is correctly imported and the symbol exists in that namespace.")
        # 2. else look in current ns
        # print(self.name)
        if n in self.names:
            if isinstance(v := self.names[n], Var) and deref_var:
                return v.deref()
            return v
        # 3. lastly, look in the referred namespaces
        for refd_ns in self.referred:
            if n in refd_ns.names:
                if isinstance(v := refd_ns.names[n], Var) and deref_var:
                    return v.deref()
                return v
        raise UnresolvedSymbolError(symbol)
    def require_ns(self, ns):
        self.namespaces[ns.name] = ns
    def include_ns(self, ns):
        self.require_ns(ns)
        self.referred.append(ns)