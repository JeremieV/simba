from os import wait
import sys, traceback
import antlr4
import src.sexprs_reader_printer
from src.simbaTypes import * 

repl_env = {
    '+': lambda a,b: a+b, # replace by sum
    '-': lambda a,b: a-b, # - sum
    '*': lambda a,b: a*b, # product
    '/': lambda a,b: int(a/b), # remove the int()
    'set': lambda x: ,
    'find': ,
    'get':,
}

_read_str  = src.sexprs_reader_printer.read_str
_print_ast = src.sexprs_reader_printer.to_string

def read_sexp(stream): # returns a SymbolicExpression
    # read_sexp the frontmatter
    return _read_str(stream)

def eval_sexp(sexp, env):
    if (isinstance(sexp, Symbol)): # if symbol evaluate to its binding
        try: return env[sexp]
        except KeyError: raise UnresolvedSymbolError(sexp)
    # elif map
    # elif vector
    elif (isinstance(sexp, SymbolicExpression)): # apply the symbolic expression
        if (sexp.positional == 0): return None
        ## Special Forms: ##
        head = sexp.positional[0]
        if "def" == head:
            a1, a2 = sexp.positional[1], sexp.positional[2]
            res = eval_sexp(a2, env)
            return env.set(a1, res)
        elif "let" == head:
            a1, a2 = sexp.positional[1], sexp.positional[2]
            let_env = Env(env)
            for i in range(0, len(a1), 2):
                let_env.set(a1[i], eval_sexp(a1[i+1], let_env))
            return eval_sexp(a2, let_env)
        else: ## Non-Special Forms ##
            ## evaluate the args ##
            evaledPArgs = [eval_sexp(e, env) for e in sexp.positional] # map(lambda e: eval_sexp(e, env), sexp.positional)
            evaledRArgs = {eval_sexp(key, env): eval_sexp(value, env) for key, value in sexp.relational}
            ## apply the head ##
            return evaledPArgs[0](*evaledPArgs[1:], **evaledRArgs)
    else: # if the value is a AtomicDatatype, cannot evaluate further
        return sexp

def print_sexp(sexp):
    _print_ast(sexp)

def simba_repl():
    eof = False
    while not eof:
        try:
            line   = input('>>> ')
            result = eval_sexp(read_sexp(line), repl_env)
            print(f'=== {result}')
            # print(rep(antlr4.StdinStream(encoding='utf-8')))
        except EOFError:
            eof = True
        except KeyboardInterrupt:
            print('Exit with Ctrl-D')
            eof = True
        except Exception as e:
            print("".join(traceback.format_exception(*sys.exc_info())))

# def run(file):
#     input  = antlr4.FileStream(file, encoding='utf-8')
#     with open(file, 'r') as f:
#         code       = f.read_sexp()
#         unindented = reader.addIndentationTokens(code)
#         ds         = reader.read_sexp(antlr4.InputStream(unindented), {})
#         result     = eval_sexp(ds, {})
#         print(result)

# when called with no arguments, the command is a terminal repl
if __name__ == "__main__" and len(sys.argv) == 1:
    simba_repl()
# when called with the name of a file, will interpret that file
elif __name__ == "__main__" and len(sys.argv) > 1:
    # run(sys.argv[1])
    pass


    
# lexer = simbaLexer(StdinStream())
# stream = CommonTokenStream(lexer)
# parser = simbaParser(stream)
# tree = parser.hi()
# printer = simbaPrintListener()
# walker = ParseTreeWalker()
# walker.walk(printer, tree)

# input  = FileStream(filename, encoding='utf-8') if filename else StdinStream(encoding='utf-8')