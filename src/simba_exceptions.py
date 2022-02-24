class SimbaException(Exception): pass

class MultipleDispatchException(SimbaException): pass

class UnresolvedSymbolError(SimbaException): pass

class SimbaSyntaxError(SimbaException): pass

class IllegalArgumentException(SimbaException): pass