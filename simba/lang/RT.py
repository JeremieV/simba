# Module containing some of the base functions for simba.
# Date created: 28 January 2022
# Author: Jérémie Vaney

import functools as ft
import itertools as it
import operator as op
from math import prod
from types import LambdaType

import pyrsistent
from simba.lang.Interfaces import ISeq
from simba.lang.types import PersistentMap, PersistentVector, Symbol
from simba.lang.PersistentList import PersistentList
from simba.exceptions import IllegalArgumentException, SimbaException
import simba.helpers as helpers
import time
import toolz

import collections.abc


def sb_apply(fn, *args, **kwargs):
    """Function application. Conses all the arguments between the first and the last to the last.
    Also applies any keyword arguments to the function."""
    arglist = []
    for e in args[:-1]:
        arglist.append(e)
    arglist = arglist + [*args[-1]]
    return fn(*arglist, **kwargs)

def sb_add(x, y):
    if x is None:
        return y
    if y is None:
        return None
    return x + y

def sb_print(e):
    from simba.simba import print_sexp
    print(print_sexp(e))

def sb_seq(seqable):
    """Returns an appropriate sequence representation of an object.
    If the sequable is empty, return nil."""
    if isinstance(seqable, collections.abc.Sequence):
        if len(seqable) == 0:
            return None
        return PersistentList.create(*seqable)
    if isinstance(seqable, PersistentMap):
        if len(s := seqable.items()) == 0:
            return None
        return s
    elif isinstance(seqable, dict):
        return PersistentList.create(*seqable.items())
    elif isinstance(seqable, PersistentList):
        return seqable
    elif seqable is None:
        return None
    else:
        raise SimbaException(f"Don't know how to make a seq from {type(seqable)}")

def sb_prepend_sexp(e, seq):
    """Defines a generic prepend function that should work on all sequence types.
    Returns an object of the same type as the second argument.
    If second arg is None, defaults to a SymbolicExpression"""
    if seq is None:
        return PersistentList.create(e)
    # elif isinstance(seq, tuple):
    #     return (e,) + seq
    # elif isinstance(seq, list):
    #     return [e] + seq
    # elif isinstance(seq, SymbolicExpression):
    return PersistentList.create(e) + PersistentList.create(*seq)

def sb_generic_concat(a, b = None):
    """Python has no built-in way of concatenating sequences of different types.
    However, this is often needed in Simba to perform generic operations on sequences.
    This function covers the built-in Python sequences and always returns a sequence
    of the same type as the first value."""
    # TODO: also define a function that works on n parameters
    if b is None:
        return a
    if a is None:
        return b
    if isinstance(a, str):
        return a + str(b)
    elif isinstance(a, tuple):
        return a + tuple(b)
    elif isinstance(a, list):
        return a + list(b)
    elif isinstance(a, PersistentList):
        return a + PersistentList.create(*b)

# def sb_uniform_access(*attrs):
#     """This implements the Uniform Access Principle.
#     Coined in Object-Oriented Software Construction by Bertrand Meyer:
#     'All services offered by a module should be available through a uniform notation, which does not betray whether they are implemented through storage or through computation.'
#     - https://en.wikipedia.org/wiki/Uniform_access_principle
#     - http://wiki.c2.com/?UniformAccessPrinciple"""
#     obj = attrs[-1]
#     attr = attrs[0]
#     if isinstance(attr, Symbol):
#         attr = attr.name
#     args = attrs[1:-1]
#     if hasattr(obj, attr):
#         a = getattr(obj, attr)
#         if callable(a) and not isinstance(a, LambdaType):
#             return eval(f"obj.{attr}")(*args)
#         else:
#             return a
#     raise SimbaException(f"{obj} has no attribute {attr}")

# def seq(coll):
#     # if isinstance(coll, Seq):
#     #     return coll
#     # else:
#     return seqFrom(coll)

seq = sb_seq

def seqFrom(coll):
    # TBD
    if hasattr(coll, 'seq'):
        return coll.seq()
    elif coll is None:
        return None
    # elif hasattr(coll, '__iter__'): # if iterable
    #     return
    else:
        raise IllegalArgumentException("Don't know how to create Seq from: " + type(coll))

# else if(coll instanceof Iterable)
#     return chunkIteratorSeq(((Iterable) coll).iterator());
# else if(coll.getClass().isArray())
#     return ArraySeq.createFromObject(coll);
# else if(coll instanceof CharSequence)
#     return StringSeq.create((CharSequence) coll);
# else if(coll instanceof PersistentMap)
#     return seq(((PersistentMap) coll).entrySet());
# else {
#     Class c = coll.getClass();
#     Class sc = c.getSuperclass();
#     throw new IllegalArgumentException("Don't know how to create ISeq from: " + c.getName());
# }

def conj(coll, x):
    if coll == None:
        return PersistentList.create(x)
    if isinstance(coll, PersistentVector):
        return coll.append(x)
    if isinstance(coll, PersistentMap):
        # return coll.set(x[], x[])
        print(x)
        return None
    return coll.cons(x)

def cons(x, seq):
    if seq is None:
        return PersistentList.create(x)
    if hasattr(seq, 'cons'):
        return seq.cons(x)
    # temporary
    if isinstance(seq, PersistentVector):
        return PersistentList.create(x, *seq)
    raise Exception()

def first(x):
    if isinstance(x, ISeq):
        return x.first()
    s = seq(x)
    if s is None:
        return None
    return s.first()

def second(x):
    return first(next(x))

def third(x):
	return first(next(next(x)))

def fourth(x):
	return first(next(next(next(x))))

def next(x):
    if isinstance(x, ISeq):
        return x.next()
    s = seq(x)
    if s is None:
        return None
    return s.next()

def more(x):
    if isinstance(x, ISeq):
        return x.more()
    s = seq(x)
    if s is None:
        return PersistentList.empty
    return s.next()

def assoc(coll, key, val):
    if coll is None:
        return PersistentMap.create({key, val})
    return coll.__setitem__(key, val),

def throw(e): raise e

# define operators that are infix in Python
repl_env = {
    'macro?': lambda obj: True if obj.macro else False, # need the environment as a param

    # arithmetic
    '+': lambda *a: ft.reduce(sb_add, a),
    '-': lambda a, *s: a-sum(s) if s else -a,
    '*': lambda *a: prod(a),
    '/': lambda a, *b: a / prod(b),
    '%': lambda a, b: b % a,
    'pow': lambda a, b: a ** b,
    'floordiv': lambda a, b: a // b,

    # comparison
    '=': lambda a, b: a == b,
    '!=': lambda a, b: a != b,
    '>': lambda a, b: a > b,
    '<': lambda a, b: a < b,
    '<=': lambda a, b: a <= b,
    '>=': lambda a, b: a >= b,

    # identity
    'is': lambda a, b: a is b,
    'is-not': lambda a, b: a is not b,

    # logic
    'not': lambda a: not a,
    'and': lambda a, b: a and b,
    'or': lambda a, b: a or b,
    # 'nand':
    # 'xor':

    # membership
    'in': lambda a, b: a in b,
    'not-in': lambda a, b: a not in b,

    # bitwise
    '&': lambda a, b: a & b,
    '|': lambda a, b: a | b,
    '^': lambda a, b: a ^ b,
    '~': lambda a: ~a,
    '<<': lambda a, b: a << b,
    '>>': lambda a, b: a >> b,

    # types
    # 'sexp': SymbolicExpression,
    'symbol': Symbol,
    'PersistentVector': PersistentVector,
    'vector': pyrsistent.v,
    'tuple': tuple,
    't': lambda *t: t,
    'HashMap': PersistentMap,
    'hash-map': pyrsistent.pmap,
    'set': set,
    'IllegalArgumentException': IllegalArgumentException,

    # magic or dunder methods: https://rszalski.github.io/magicmethods/
    'new': lambda obj, *args, **kwargs: obj(*args, **kwargs),
    'del': lambda obj: obj.__del__(),
    'at': lambda i, obj: obj[i], # 'get-item'
    'set-at': lambda i, new, obj: obj.__setitem__(i, new),
    'del-at': lambda i, obj: obj.__delitem__(i),
    # I would like to have
    # - special syntax for get, set, del
    # - universal access principle, such that if attr doesn't exist, then tries to call method
    # 'get-attr': sb_uniform_access, # lambda attr, obj: obj.__getattribute__(attr),
    'set!': lambda obj, attr, value: obj.__setattr__(attr, value),
    'del-attr': lambda attr, obj: obj.__delattr__(attr),

    # sequences
    'count': toolz.count,
    'between': lambda low, up = None, seq = None: seq[low:up] if seq is not None else up[low:],
    'prepend-sexp': sb_prepend_sexp,
    'prepend': lambda *es: list(es[:-1] + tuple(es[-1])),
    # 'append': sb_append,
    'concat': sb_generic_concat, # lambda *lists: ft.reduce(op.add, lists), # this poses certain problems bc its the add operation
    'reverse': helpers.reverse,
    'range': range,

    # collections

    # IO
    'print': (lambda *args: [sb_print(e) for e in args][0]),
    'prn': (lambda *args: [print(e, end = "") for e in args][0]),
    'throw': throw,

    # reflection
    # interop
    'get': lambda e, obj: obj[e],
    'date': time.time,
    'py-exec': helpers.exec_with_return,
}