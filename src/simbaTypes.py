"""
The data types for the Simba interpreter.
Naming convention?
Many data types are declared as aliases for the benefit of being able to call isinstance() to determine type (Maybe this is a bad idea).
"""
from re import split
import helpers

# Atomic Data Types
class Symbol:
    def __init__(self, string):
        split_str = split('/', string)
        if string == '/': self.name = '/'; self.namespace = None
        elif len(split_str) > 2: raise SyntaxError("A symbol can only have one namespace qualifier.")
        elif len(split_str) == 2:
            if split_str[0] == '' or split_str[1] == '': raise SyntaxError("None of the two members of the symbol should be empty.")
            self.namespace = split_str[0]
            self.name = split_str[1]
        elif len(split_str) == 1:
            if split_str[0] == '': raise SyntaxError("A symbol cannot be empty (duh).")
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

# class Keyword(str): pass
Number = (int, float)
# String = str
# AtomicDatatype = (String, Number)
Environment = dict

true = True
false = False

# Symbolic Data Types

class SymbolicExpression():
    """A symbolic expression contains: symbol, positional arguments, relational arguments"""
    name = ""
    def __init__(self, *args, **kwargs):
        self.positional = []
        for e in args:
            self.positional.append(e)
        if (kwargs): self.relational = kwargs
        else: self.relational = {}

    def append(self, e):
        self.positional.append(e)

    def __repr__(self):
        return str(self.positional)

    def __getitem__(self, __slice):
        if isinstance(__slice, slice):
            return self.positional[__slice.start: __slice.stop]
        else:
            return self.positional[__slice]

    def __eq__(self, __o):
        if not isinstance(__o, SymbolicExpression): return False
        return all(value == __o[i] for i, value in enumerate(self.positional))

    def __add__(self, sexp):
        if isinstance(sexp, SymbolicExpression):
            self.positional = self.positional + sexp.positional
            return self
        # elif isinstance(sexp, tuple):
        #     self.positional = self.positional + SymbolicExpression(sexp).positional
        #     return self
        else:
            raise Exception(f"Tried to concat SymbolicExpression with unsupported type {type(sexp)}")



# Collection Data Types

List = list
Vector = list
Map = dict

class PersistentVector():
    """This is a persistent vector"""

class  PersistentMap():
    """This is a persistent map"""

class Protocol():
    """This is the protocol type"""

# a = SymbolicExpression(1, 2, 3, a=3, b=6)
# a.append()
# print(a.positional, a.relational)

# =====================
#      Exceptions
# =====================

class UnresolvedSymbolError(Exception): pass

# =====================
#       INTERNAL
# =====================

class SimbaEnvironment():
    """Just like a scheme environment. Contains a mapping of symbols to namespaces and an outer environment.
    An addition that is made to the typical environment"""
    def __init__(self, outer = None, names = {}, namespaces = {}, referred = []):
        self.outer = outer
        self.names = names
        self.namespaces = namespaces
        self.referred = referred
    def set(self, symbol, value):
        """Change or add a binding. The binding has to be in the local namespace."""
        # there is a bug here: what if the current namespace is qualified! we could just add the current ns as param to __init__
        if symbol.namespace != None: raise("Cannot change a binding outside of current namespace.")
        env = self.find(symbol)
        if env is None or env is self:
            self.names[symbol.name] = value
        else:
            env.set(symbol, value)
    def find(self, symbol):
        """Looks for a binding, first in current env, and then in outer, and so on. Returns the env where the match is made first.
        If the symbol is namespace-qualified, look for the binding directly in that namespace."""
        # there is a bug here bc you have to look in the namespaces of the outer envs also
        ns = symbol.namespace
        if ns is not None:
            # there is a bug here bc if the namespace is qualified to be the current ns
            if ns in self.namespaces:
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
        strkey = symbol.name
        # there is a bug here bc you have to look in the namespaces of the outer envs also
        # if symbol.namespace != None: return self.namespaces[strkey].get(symbol)
        if strkey in self.names:
            return self.names[strkey]
        location = self.find(symbol)
        if location is None:
            raise UnresolvedSymbolError(strkey)
        return location.get(symbol)
    def require_ns(self, ns_name:str, ns):
        self.namespaces[ns_name] = ns
    def include_ns(self, name, ns):
        self.require_ns(name, ns)
        self.referred.append(ns)
        # it's also possible to refer individual names by creating small namespaces