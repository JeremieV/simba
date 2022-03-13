class SimbaException(Exception):
    def __init__(self, message, sexp, env, namespace):
        self.message = message
        self.sexp = sexp
        self.env = env
        self.namespace = namespace
        super().__init__(self.message)
    def __str__(self):
        from simba import print_sexp
        return f"""{super().__str__()}
In {print_sexp(self.sexp)}
{f"In namespace {self.namespace}" if self.namespace else ""}"""

class SimbaSyntaxError(SimbaException): pass

class MultipleDispatchException(SimbaException): pass

class UnresolvedSymbolError(SimbaException): pass

class SimbaSyntaxError(SimbaException): pass

class IllegalArgumentException(SimbaException): pass

class MultipleNamespacesError(SimbaException): pass

class NoNamespaceError(SimbaException): pass

class ImmutableBindingException(SimbaException): pass

class FailingGuardException(SimbaException): pass

class MultiMethodException(SimbaException): pass