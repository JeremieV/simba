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
        if self.namespace: return '/'.join(self.namespace, self.name)
        else: return self.name
    def __repr__(self):
        return str(self)

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
    # def __init__(self, head, positional, relational):
    #     self.head: str = head
    #     self.positional: list = positional
    #     self.relational: dict = relational
        # sefl.meta = {} # meta should hold information such as line number and types maybe

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
    def __init__(self, outer = None, names = {}, namespaces = {}):
        self.outer = outer
        self.names = names
        self.namespaces = namespaces
    def set(self, key, value):
        """Change or add a binding. The binding has to be in the local namespace."""
        env = self.find(key)
        if env is None or env is self:
            self.names[key] = value
        else:
            env.set(key, value)
    def find(self, key):
        """Looks for a binding, first in current env, and then in outer, and so on. Returns the env where the match is made first."""
        if str(key) in self.names:
            return self
        if self.outer is not None:
            return self.outer.find(key)
        return None
    def get(self, key):
        """Returns the binding if it is in current env or parents."""
        strkey = str(key)
        if strkey in self.names:
            return self.names[strkey]
        location = self.find(key)
        if location is None:
            raise UnresolvedSymbolError(strkey)
        return location.get(key)
    def add_ns(self, ns_name:str, ns):
        self.namespaces[ns_name] = ns