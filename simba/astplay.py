import inspect

def do(*exprs):
    return exprs[-1]

class fn:
    def __init__(self, doc, *fns):
        self.n_args = True # True at the beginning, None when varargs, int else
        self.__meta__ = {}
        if isinstance(doc, str):
            self.__doc__ = doc
        elif isinstance(doc, dict):
            if 'doc' in doc: self.__doc__ = doc['doc']
            self.__meta__ = doc
        else:
            fns = (doc,) + fns
        self.method_table = []
        for fn in fns:
            self.register(fn)
    def register(self, fn):
        if self.n_args is not None:
            argspec = inspect.getfullargspec(fn)
            sig = None if argspec.varargs else len(argspec.args)
            if sig is not None and self.n_args is not True and sig <= self.n_args:
                raise Exception("Incoherent arities for the fn")
            self.n_args = sig
            self.method_table.append((sig, fn))
        else:
            raise Exception("Already a vararg arity for the fn")
    def clear(self):
        self.method_table = []
    def signatures(self):
        r = []
        for t in self.method_table:
            r.append(t[0])
        return r
    def __call__(self, *p_args):
        for tup in self.method_table:
            if tup[0] is None or len(p_args) == tup[0]:
                return tup[1](*p_args)
        raise Exception(f"No matching signature for multimethod")