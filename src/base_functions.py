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

def sb_prepend_sexp(e, sexp:SymbolicExpression):
    if sexp is None:
        return SymbolicExpression(e)
    sexp.positional = [e] + sexp.positional
    return sexp

def macroexpand(ast, env):
    while is_macro_call(ast, env):
        mac = env.get(ast[0])
        ast = mac(*ast[1:])
    return ast

repl_env = {
    # predicates
    'is-instance': isinstance,
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
    'vector': lambda *a: [*a],
    # map

    # sequences
    'len': len,
    'slice': lambda low, up = None, seq = None: seq[low:up] if seq is not None else up[low:],
    'nth': lambda i, obj: obj[i],
    'prepend-sexp': sb_prepend_sexp,
    'prepend': lambda e, coll: [e] + coll,
    'append': sb_append,
    'concat': lambda *lists: ft.reduce(op.add, lists), # this poses certain problems bc its the add operation
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
}

def sb_print(e):
    from simba import print_sexp
    print(print_sexp(e))
