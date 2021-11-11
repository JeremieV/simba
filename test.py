import dis  # disassembler
import parser  # -- deprecated
import ast  # new one

# Other VM types than stack-oriented?
# Anything that looks like a graph?

def fib(n):
    if n < 2:
        return n
    current, next = 0, 1
    while n:
        current, next = next, current + next
        n -= 1
    return current

# built in

fib.__code__
fib.__code__.co_varnames # and more ...

dir(fib.__code__)
parser.__doc__

# dis

dis.dis(fib)
dis.dis("{}")
dis.dis("dict()")

# ast

print(ast.dump(ast.parse('123', mode='eval'), indent=4))

