#! python3
import sys, traceback
sys.path.insert(0, '/Users/jeremievaney/Desktop/language')
from os import wait
# import antlr4
import sexprs_reader_printer
import dotexprs_reader_printer
from simbaTypes import *
import importlib
import helpers

import functools
from math import prod

# _reader    = sexprs_reader_printer.SexpReader
# _read_form  = sexprs_reader_printer.read_str
# _print_ast = sexprs_reader_printer.to_string
_reader = sexprs_reader_printer

default_syntax = sexprs_reader_printer

def read_sexp(string, syntax = default_syntax): # returns a SymbolicExpression
    # read the frontmatter
    return syntax.read_str(string)

class Function:
    """Functions are anonymous, but optionally named."""
    def __init__(self, params, ast, bindings, loaded_ns, name = None):
        self.name = name
        self.args = params
        self.ast  = ast
        self.bindings = bindings # the bindings should hold the bindings from the args and closure
        self.loaded_ns = loaded_ns
    
    def __call__(self, *e_p_args, **e_r_args):
        # a fn should have no dynamically bound symbols in it.
        # Its environment consists in the args + enclosed free variables at the time of creation
        # how to I do efficient binding and binding of relational arguments?
        # print ({self.args[i]: e_p_args[i] for i in range(len(e_p_args))})
        res =  None
        env = SimbaEnvironment(
                outer=self.bindings,
                names={self.args[i].name: e_p_args[i] for i in range(len(e_p_args))}
            )
        for e in self.ast:
            # evaluate in an implicit do loop #
            res = ns_eval_sexp(e, env = env, loaded_namespaces=self.loaded_ns)
        return res

def eval_sexp(sexp, env):
    """
    eval_exp evaluates a Symbolic Expression within a context.
    The context is the 'environment' a mapping of names to namespaces,
    and the namespace in which the execution is working at the moment.
    By default, execution starts in the `None` namespace, which corresponds to the standard library.
    """
    if (isinstance(sexp, Symbol)): # if symbol evaluate to its binding
        try: return env.get(sexp)
        except KeyError: raise UnresolvedSymbolError(sexp)
    # elif map
    # elif vector
    elif (isinstance(sexp, SymbolicExpression)): # apply the symbolic expression
        if len(sexp.positional) == 0:
            return None
        ## Special Forms: ##
        head = sexp.positional[0]
        if "def" == head.name:
            ## def adds a binding (from unevaluated first arg to evaled second arg) in the environment ##
            a1, a2 = sexp.positional[1], sexp.positional[2]
            res = eval_sexp(a2, env)
            return env.set(a1, res)
        elif "quote" == head.name:
            if len(sexp.positional) != 2: raise Exception("quote expected 1 argument")
            return sexp.positional[1]
        elif "if" == head.name:
            ## If may need some more work: what is truthy? what if fewer then 3 args? ##
            if (len(sexp.positional) < 3):
                raise SyntaxError("Too few arguments to if")
            if (len(sexp.positional) > 4):
                raise SyntaxError("Too many arguments to if")
            cond, then = sexp.positional[1:3]
            if cond:
                return eval_sexp(then, env)
            else:
                if (len(sexp.positional) == 4):
                    _else = sexp.positional[3]
                    return eval_sexp(_else, env)
                else: return None
        elif "fn" == head.name:
            ## Anonymous function ##
            ## returns a new closure ##
            argVector, body = sexp.positional[1], sexp.positional[2:]
            # what the closure should do is:
            # - gather all the free variables
            # - point to the local bindings in `bindings`
            bindings = env # this is temporary: 
            # for now, the entire enclosing scope in copied
            # in the future, the bindings will be only the ones references in the closure
            return Function(argVector, body, bindings)
        elif "do" == head.name:
            last = None
            for exp in sexp.positional[1:]:
                last = eval_sexp(exp, env)
            return last
        elif "comment" == head.name:
            return None
        elif "let" == head.name:
            ## creates a new environment and binds the values to it successively (in order) ##
            vec, body = sexp.positional[1], sexp.positional[2:]
            let_env = SimbaEnvironment(outer = env)
            for i in range(0, len(vec), 2):
                let_env.set(vec[i], eval_sexp(vec[i+1], let_env))
            ## evaluate the body in an implicit do ##
            last = None
            for exp in body:
                last = eval_sexp(exp, let_env)
            return last
        # elif type(head) == function:
        #     ## Call a native function ##
        #     return head(*sexp.positional[1:], **sexp.relational)
        elif "ns" == head.name:
            # ## If the namespace is 
            # ## add a ns to the environment, and "jump" into it for evaluation ##
            # if len(sexp.positional) != 2:
            #     raise SyntaxError("The `namespace` form should have one argument.")
            # # 1. Initialize the namespace and add it to the namespaces
            # new_ns = sexp.positional[1]
            # namespaces[new_ns] = SimbaEnvironment()
            # # 2. Jump into the namespace to start evaluation

            # print(env)
            last = None
            for exp in sexp.positional[2:]:
                last = eval_sexp(exp, env)
            return last
        else:
            ## Non-Special Forms ##
            ## evaluate the args ##
            evaledPArgs = [eval_sexp(e, env) for e in sexp.positional]
            evaledRArgs = {eval_sexp(key, env): eval_sexp(value, env) for key, value in sexp.relational}
            ## apply the head ##
            return evaledPArgs[0](*evaledPArgs[1:], **evaledRArgs)
    else: # if the value is an atomic data type, cannot evaluate further
        return sexp

# def eval_str(string):
#     exec_environment = SimbaEnvironment(names = repl_env)
#     readerObj = _reader.SexpReader(string)
#     result = None
#     while readerObj.position < len(readerObj.tokens):
#         e = readerObj.read_form()
#         result = eval_sexp(e, exec_environment)
#     return result

def print_sexp(sexp, syntax = default_syntax) -> str:
    return syntax.to_string(sexp)

def convert(string, _from, to):
    return to.print_sexp(_from.read_sexp(string))

# def simba_import(module):
#     importlib.import_module(module)

repl_env = {
    '+': lambda *a: sum(a),
    '-': lambda a, *s: a-sum(s) if s else -a,
    '*': lambda *a: prod(a),
    '/': lambda a, *b: a / prod(b),
    '%': lambda a, b: a % b,
    'print': (lambda *args: [print(print_sexp(e)) for e in args][0]),
    # 'import': lambda module: importlib.import_module(module)
    '=': lambda a, b: a == b,
    'not': lambda a: not a
}

def eval_form(env, form, print_result = False):
    result = eval_sexp(form, env)
    if print_result: print(print_sexp(result))

def simba_repl():
    eof = False
    _env = SimbaEnvironment(names = repl_env)
    while not eof:
        try:
            line = input('>>> ')
            helpers.read_string_form_by_form(_reader,
                functools.partial(eval_form, _env, print_result = True), line)
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

            # print(rep(antlr4.StdinStream(encoding='utf-8')))

# lexer = simbaLexer(StdinStream())
# stream = CommonTokenStream(lexer)
# parser = simbaParser(stream)
# tree = parser.hi()
# printer = simbaPrintListener()
# walker = ParseTreeWalker()
# walker.walk(printer, tree)

# input  = FileStream(filename, encoding='utf-8') if filename else StdinStream(encoding='utf-8')

# ===================
# namespaces: execution environment
# eval: for any given file, starts evaling in the None namespace.
# whenever encounters a use, *if* the namespace is not used yet, run it, else, just add a ref to it in the current environment
# then, for every symbol, if the symbol is qualified, then fetch it in the corresponding environment.

# access top level vars
# every symbol can be namespace-qualified: add a slot to symbol

# load a namespace
# what does require do? ????? ??????? ??? ?? ? ?? ? ?? ? ?? ?? ?? ?? ??

def ns_eval_sexp(sexp, env, loaded_namespaces):
    """
    eval_exp evaluates a Symbolic Expression within a context.
    The context is the 'environment' a mapping of names to namespaces,
    and the namespace in which the execution is working at the moment.
    By default, execution starts in the `None` namespace, which corresponds to the standard library.
    """
    if (isinstance(sexp, Symbol)): # if symbol evaluate to its binding
        try: return env.get(sexp)
        except KeyError: raise UnresolvedSymbolError(sexp)
    # elif map
    # elif vector
    elif (isinstance(sexp, SymbolicExpression)): # apply the symbolic expression
        if len(sexp.positional) == 0:
            return None
        ## Special Forms: ##
        head = sexp.positional[0]
        if "def" == head.name:
            ## def adds a binding (from unevaluated first arg to evaled second arg) in the environment ##
            a1, a2 = sexp.positional[1], sexp.positional[2]
            res = ns_eval_sexp(a2, env, loaded_namespaces)
            return env.set(a1, res)
        elif "quote" == head.name:
            if len(sexp.positional) != 2: raise Exception("quote expected 1 argument")
            return sexp.positional[1]
        elif "if" == head.name:
            ## If may need some more work: what is truthy? what if fewer than 3 args? ##
            if (len(sexp.positional) < 3):
                raise SyntaxError("Too few arguments to if")
            if (len(sexp.positional) > 4):
                raise SyntaxError("Too many arguments to if")
            cond, then = sexp.positional[1:3]
            evaled_cond = ns_eval_sexp(cond, env, loaded_namespaces)
            if evaled_cond:
                return ns_eval_sexp(then, env, loaded_namespaces)
            else:
                if (len(sexp.positional) == 4):
                    _else = sexp.positional[3]
                    return ns_eval_sexp(_else, env, loaded_namespaces)
                else: return None
        elif "fn" == head.name:
            ## Anonymous function ##
            ## returns a new closure ##
            argVector, body = sexp.positional[1], sexp.positional[2:]
            # what the closure should do is:
            # - gather all the free variables
            # - point to the local bindings in `bindings`
            bindings = env # this is temporary: 
            # for now, the entire enclosing scope in referenced. This may impair garbage collection too much.
            # in the future, the bindings will be only the ones references in the closure
            return Function(argVector, body, bindings, loaded_namespaces)
        elif "do" == head.name:
            last = None
            for exp in sexp.positional[1:]:
                last = ns_eval_sexp(exp, env, loaded_namespaces)
            return last
        elif "comment" == head.name:
            return None
        elif "let" == head.name:
            ## creates a new environment and binds the values to it successively (in order) ##
            vec, body = sexp.positional[1], sexp.positional[2:]
            let_env = SimbaEnvironment(outer = env)
            for i in range(0, len(vec), 2):
                let_env.set(vec[i], ns_eval_sexp(vec[i+1], let_env, loaded_namespaces))
            ## evaluate the body in an implicit do ##
            last = None
            for exp in body:
                last = ns_eval_sexp(exp, let_env, loaded_namespaces)
            return last
        # elif type(head) == function:
        #     ## Call a native function ##
        #     return head(*sexp.positional[1:], **sexp.relational)
        elif "ns" == head.name:
            # 1. Initialize the namespace and add it to the namespaces
            # 2. Jump into the namespace to start evaluation
            last = None
            for exp in sexp.positional[2:]:
                last = ns_eval_sexp(exp, env, loaded_namespaces)
            return last
        elif "include" == head.name:
            # MAYBE THE NAMESPACE SHOULD ALWAYS HAVE ITSELF AS A PARENT NAMESPACE? THIS WAY I RESOLVE THE SELF-QUALIFYING PROBLEM
            ns_name = sexp.positional[1].name
            if ns_name not in loaded_namespaces:
                # creates a new environment for the new namespace
                ns_env = SimbaEnvironment(outer=loaded_namespaces['base'])
                # evaluates the content of that namespace in the new environment
                ns_eval_sexp(helpers.find_ns(ns_name, ast), ns_env, loaded_namespaces)
                # add the new namespace environment to the list of loaded namespaces
                loaded_namespaces[ns_name] = ns_env
                # add the environment to the list of contextual namespaces
                env.add_ns(ns_name, loaded_namespaces[ns_name])
            else:
                env.add_ns(ns_name, loaded_namespaces[ns_name])
        else:
            ## Non-Special Forms ##
            ## evaluate the args ##
            evaledPArgs = [ns_eval_sexp(e, env, loaded_namespaces) for e in sexp.positional]
            evaledRArgs = {ns_eval_sexp(key, env, loaded_namespaces): ns_eval_sexp(value, env, loaded_namespaces) for key, value in sexp.relational}
            ## apply the head ##
            return evaledPArgs[0](*evaledPArgs[1:], **evaledRArgs)
    else: # if the value is an atomic data type, cannot evaluate further
        return sexp


def namespaced_eval(ast_list):
    """Adds namespace functionality to the Simba evaluation.
    
    Keeps track of multiple namespaces in the namespaces variable.
    At any given time, a namespace is 'current', the current namespace is held in the ns variable. This is inspired by common lisp.
    
    The evaluation starts in the 'main' namespace. Every time a namespace is referred, that namespace the function looks for it in its
    AST representation of the program, and evaluates it if it is the first time it is referred."""
    # ns = None
    main = helpers.find_ns("main", ast_list)
    # print(main)
    res = ns_eval_sexp(main, SimbaEnvironment(names = repl_env), loaded_namespaces = {
        'base': SimbaEnvironment(names = repl_env)
    })


# when called with no arguments, the command is a terminal repl
if __name__ == "__main__" and len(sys.argv) == 1:
    simba_repl()
# when called with the name of a file, will interpret that file
elif __name__ == "__main__" and len(sys.argv) > 1:
    files = sys.argv[1:]
    ast = helpers.read_files(_reader, files)
    # print(ast)
    # main = helpers.find_ns("main", ast)
    # print(main)
    # res = eval_sexp(main, SimbaEnvironment(names = repl_env))
    res = namespaced_eval(ast)
