class SimbaException(Exception): pass

class SimbaSyntaxError(SimbaException): pass

class IllegalArgumentException(SimbaException): pass
class MultipleDispatchException(SimbaException): pass
class MultiMethodException(SimbaException): pass
class FailingGuardException(SimbaException): pass

class UnresolvedSymbolError(SimbaException): pass
class MultipleNamespacesError(SimbaException): pass
class NoNamespaceError(SimbaException): pass
class ImmutableBindingException(SimbaException): pass