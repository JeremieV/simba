# Module containing some of the base functions for simba.
# Date created: 28 January 2022
# Author: Jérémie Vaney

import functools as ft
import itertools as it
import operator as op
from math import prod
from types import LambdaType

import pyrsistent
from simba_types import Map, Vector
import helpers
from simba_types import SymbolicExpression, Symbol
import time
import toolz

import collections.abc

from simba_exceptions import SimbaException

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
    from simba import print_sexp
    print(print_sexp(e))

def sb_seq(seqable):
    """Returns an appropriate sequence representation of an object.
    If the sequable is empty, return nil."""
    if isinstance(seqable, collections.abc.Sequence):
        if len(seqable) == 0:
            return None
        return seqable
    elif isinstance(seqable, Map):
        if len(s := seqable.items()) == 0:
            return None
        return s
    elif isinstance(seqable, dict):
        return pyrsistent.pvector(seqable.items())
    elif isinstance(seqable, SymbolicExpression):
        return pyrsistent.pvector(seqable)
    elif seqable is None:
        return None
    else:
        raise SimbaException(f"Don't know how to make a seq from {type(seqable)}", None, None, None)

def sb_prepend_sexp(e, seq):
    """Defines a generic prepend function that should work on all sequence types.
    Returns an object of the same type as the second argument.
    If second arg is None, defaults to a SymbolicExpression"""
    if seq is None:
        return SymbolicExpression(e)
    # elif isinstance(seq, tuple):
    #     return (e,) + seq
    # elif isinstance(seq, list):
    #     return [e] + seq
    # elif isinstance(seq, SymbolicExpression):
    return SymbolicExpression(e) + SymbolicExpression(*seq)

def sb_generic_concat(a, b):
    """Python has no built-in way of concatenating sequences of different types.
    Howver, this is often needed in Simba to perform generic operations on sequences.
    This function covers the built-in Python sequences and always returns a sequence
    of the same type as the first value."""
    # TODO: also define a function that works on n parameters
    if b is None:
        return a
    if a is None:
        return b
    if type(a) == type(b):
        return a+b
    elif isinstance(a, tuple):
        return a + tuple(b)
    elif isinstance(a, list):
        return a + list(b)
    elif isinstance(a, SymbolicExpression):
        return a + SymbolicExpression(*b)

def sb_uniform_access(*attrs):
    """This implements the Uniform Access Principle.
    Coined in Object-Oriented Software Construction by Bertrand Meyer:
    'All services offered by a module should be available through a uniform notation, which does not betray whether they are implemented through storage or through computation.'
    - https://en.wikipedia.org/wiki/Uniform_access_principle
    - http://wiki.c2.com/?UniformAccessPrinciple"""
    obj = attrs[-1]
    attr = attrs[0]
    if isinstance(attr, Symbol):
        attr = attr.name
    args = attrs[1:-1]
    if hasattr(obj, attr):
        a = getattr(obj, attr)
        if callable(a) and not isinstance(a, LambdaType):
            return eval(f"obj.{attr}")(*args)
        else:
            return a
    raise SimbaException(f"{obj} has no attribute {attr}", None, None, None)

def throw(e): raise e

# define operators that are infix in Python
repl_env = {
    # predicates
    'instance?': isinstance, # maybe I should switch the order of arguments
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
    'sexp': SymbolicExpression,
    'symbol': Symbol,
    'Vector': Vector,
    'vector': pyrsistent.v,
    'tuple': tuple,
    't': lambda *t: t,
    'HashMap': Map,
    'hash-map': pyrsistent.pmap,
    'set': set,
    'exception': Exception,
    'type': type,
    'str': str,
    'bytes': bytes,

    # magic or dunder methods: https://rszalski.github.io/magicmethods/
    'new': lambda obj, *args, **kwargs: obj(*args, **kwargs),
    'del': lambda obj: obj.__del__(),
    'at': lambda i, obj: obj[i], # 'get-item'
    'set-at': lambda i, new, obj: obj.__setitem__(i, new),
    'del-at': lambda i, obj: obj.__delitem__(i),
    # I would like to have
    # - special syntax for get, set, del
    # - universal access principle, such that if attr doesn't exist, then tries to call method
    'get-attr': sb_uniform_access, # lambda attr, obj: obj.__getattribute__(attr),
    'set-attr': lambda attr, value, obj: obj.__delattr__(attr, value),
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