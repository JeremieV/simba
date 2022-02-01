# Module containing some of the base functions for simba.
# Date created: 28 January 2022
# Author: Jérémie Vaney

import functools as ft
import itertools as it
import operator as op
from math import prod
import helpers
from simbaTypes import SymbolicExpression

def sb_add(x, y):
    if x is None:
        return y
    if y is None:
        return None
    return x + y

def sb_append(e, coll):
    coll.append(e)
    return coll

def interop(callable, *args, **kwargs):
    return callable(*args, **kwargs)

# you need ways to: get attrs, call methods, index accurately, __instantiate classes__
def get_attribute(obj, attr):
    return obj.attr # getattr

def call_method(obj, method, *args, **kwargs):
    return obj.method(*args, **kwargs)

# def sb_prepend_sexp(e, sexp:SymbolicExpression):
#     if sexp is None:
#         return SymbolicExpression(e)
#     sexp.positional = [e] + sexp.positional
#     return sexp

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
    if type(a) == type(b):
        return a+b
    if b is None:
        return a
    if a is None:
        return b
    elif isinstance(a, tuple):
        return a + tuple(b)
    elif isinstance(a, list):
        return a + list(b)
    elif isinstance(a, SymbolicExpression):
        return a + SymbolicExpression(*b)

repl_env = {
    # predicates
    'is': lambda a, b: a is b,
    'is-instance': isinstance, # can't work for now
    'is-macro': lambda obj: True if obj.is_macro else False, # need the environment as a param

    # arithmetic
    '+': lambda *a: ft.reduce(sb_add, a),
    '-': lambda a, *s: a-sum(s) if s else -a,
    '*': lambda *a: prod(a),
    '/': lambda a, *b: a / prod(b),
    '%': lambda a, b: a % b,
    '=': lambda a, b: a == b,
    # comparison such as ≤

    # logic
    'not': lambda a: not a,
    'and': lambda a, b: a and b,
    'or': lambda a, b: a or b,
    # 'nand':
    # 'xor':

    # data structure creation
    'sexp': lambda *a, **ka: SymbolicExpression(*a, **ka),
    'vector': lambda *a: [*a],
    'tuple': lambda *a: a,
    'hash-map': lambda *a: {key: val for key, val in zip(a, a)},

    # sequences
    'count': len,
    'slice': lambda low, up = None, seq = None: seq[low:up] if seq is not None else up[low:],
    'nth': lambda i, obj: obj[i],
    'prepend-sexp': sb_prepend_sexp,
    'prepend': lambda e, coll: [e] + coll,
    'append': sb_append,
    'concat': sb_generic_concat, # lambda *lists: ft.reduce(op.add, lists), # this poses certain problems bc its the add operation
    'reverse': helpers.reverse,

    # collections

    # IO
    'print': (lambda *args: [sb_print(e) for e in args][0]),
    'prn': (lambda *args: [print(e, end = "") for e in args][0]),
    # 'import': lambda module: importlib.import_module(module)
    # 'time': timeit.timeit

    # reflection
    # interop
    'get': getattr,
    'type': type,
    'locals': locals,
}

def sb_print(e):
    from simba import print_sexp
    print(print_sexp(e))