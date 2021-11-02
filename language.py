import sys, traceback

in_prompt = ">>> "
out_prompt = ""

def read(input):
    input()

def eval(ast, env):
    return ast

def print(exp):
    return exp

def rep():
    while (True):
        print(eval(read(str, {})))

while True:
    try:
        print("")
        line = input()
        print(rep(line))
    except Exception as e:
        print("".join(traceback.format_exception(*sys.exc_info())))