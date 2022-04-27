import inspect

# Clownjure
# - programming with expressions
# - immutability by default
# - managed references
# - programming to abstractions (protocols)
# - macros!

class Var: pass
class Atom: pass
class Keyword(str): pass
class Symbol(str): pass
# ---
class Vector: pass
class List: pass
class Map: pass

# if, let, do, define, fn, quote??

def do(*exprs):
    return exprs[-1]

def define(name, value):
    globals()[name] = value

def let(pvec, *args):
    l = locals()
    for i in range(0, len(pvec), 2):
        l[pvec[i]] = l[pvec[i+1]]
    return do(*args)

# fn is quite a bit more complicated
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

# but the multifunction comes easy
class multifn:
    def __init__(self, dispatch_fn):
        self.dispatch_fn = dispatch_fn
        self.method_table = {} # a mapping of dispatch-value to functions
    def register(self, dispatch_value, fn):
        if dispatch_value in self.method_table:
            raise Exception(f"The dispatch value {dispatch_value} is already registered for the multimethod.")
        self.method_table[dispatch_value] = fn
    def methods(self):
        """Returns a list of the registered dispatch values on the multimethod."""
        return self.method_table.keys()
    def __call__(self, *args):
        # evaluate the dispatch function
        dispatch_val = self.dispatch_fn(*args)
        # if val not in dict dispatch to the default fn
        if dispatch_val not in self.method_table:
            try:
                f = self.method_table["default"]
            except KeyError:
                raise Exception(f"Tried to fall back to the default method but no such method exists.")
        else:
            f = self.method_table[dispatch_val]
        return f(*args)

# --- standard library

# ---

a = fn(
    lambda x: x,
    lambda x, y: x + y
)

m = multifn(lambda x : x)

m.register (None,
    lambda x: print("It was none")
)

m.register (3,
    lambda x: print("It was 3")
)

# print(m(None))


# a = list(map(inc, range(500001)))

# print(a[500000])

import pyrsistent as p

print(p.plist((1, 2)))