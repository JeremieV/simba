"""
The data types for the Simba interpreter.
Naming convention?
Many data types are declared as aliases for the benefit of being able to call isinstance() to determine type (Maybe this is a bad idea).
"""

# Atomic Data Types
class Symbol(str): pass   ## Symbol derives string but is distinct ##
# class Keyword(str): pass
Number = (int, float)
String = str
AtomicDatatype = (String, Number)

Environment = dict

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
    pass