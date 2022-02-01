#! python3
import sys, traceback

sys.path.insert(0, '.')
# import antlr4
import sexprs_reader_printer
import dotexprs_reader_printer
from simbaTypes import *
import importlib
import helpers
import timeit

import functools
import prompt_toolkit
import argparse

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
    def __init__(self, params, ast, bindings, loaded_ns, name = None, is_macro = False):
        self.name = name
        self.args = params
        self.ast  = ast
        self.bindings = bindings # the bindings should hold the bindings from the args and closure
        self.loaded_ns = loaded_ns
        self.is_macro = is_macro
    
    def __call__(self, *e_p_args, **e_r_args):
        # a fn should have no dynamically bound symbols in it.
        # Its environment consists in the args + enclosed free variables at the time of creation
        names = {}
        for i, arg in enumerate(self.args):
            if arg.name == '&':
                names[self.args[i+1].name] = e_p_args[i:]
                break
            else:
                names[arg.name] = e_p_args[i]

        res =  None
        env = SimbaEnvironment(
                outer=self.bindings,
                names=names
            )
        for e in self.ast:
            # evaluate in an implicit do loop #
            res = ns_eval_sexp(e, env = env, loaded_namespaces=self.loaded_ns)
        return res

def print_sexp(sexp, syntax = default_syntax) -> str:
    return syntax.to_string(sexp)

from base_functions import repl_env

def convert(string, _from, to):
    return to.print_sexp(_from.read_sexp(string))

# def simba_import(module):
#     importlib.import_module(module)

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

def quasiquote(ast):
    if isinstance(ast, Symbol) or isinstance(ast, Map): 
        return SymbolicExpression(Symbol('quote'), ast)
    elif isinstance(ast, SymbolicExpression) and ast[0] == Symbol("unquote"):
        return ast[1]
    elif isinstance(ast, SymbolicExpression):
        res = SymbolicExpression()
        for e in helpers.reverse(ast.positional):
            if isinstance(e, SymbolicExpression) and e[0] == Symbol("splice-unquote"):
                res = SymbolicExpression(Symbol('concat'), e[1], res)
            else:
                res = SymbolicExpression(Symbol('prepend-sexp'), quasiquote(e), res)
        return res
    else:
        return ast

def is_macro_call(ast, env):
    if isinstance(ast, SymbolicExpression) and len(ast.positional) != 0 and isinstance(ast[0], Symbol):
        try:
            refers_to = env.get(ast[0])
        except:
            refers_to = None
        if isinstance(refers_to, Function) and refers_to.is_macro == True:
            return True
    return False

def macroexpand(ast, env):
    """This is the most basic macroexpansion algorithm possible:
    While the head of the expression resolves to a macro, the corresponding
    macro function is called on its **unevaluated** arguments.
    """
    while is_macro_call(ast, env):
        macro_fn = env.get(ast[0])
        args = ast[1:]
        ast = macro_fn(*args)
        # print(ast)
    return ast

def ns_eval_sexp(sexp, env, loaded_namespaces = {}):
    """
    `ns_eval_exp` evaluates a Symbolic Expression within a context.
    The context is the 'environment' a mapping of names to namespaces,
    and the namespace in which the execution is working at the moment.
    By default, execution starts in the `None` namespace, which corresponds to the standard library.
    """
    # macroexpansion step
    sexp = macroexpand(sexp, env)
    if (isinstance(sexp, Symbol)): # if symbol evaluate to its binding
        try: return env.get(sexp)
        except KeyError: raise UnresolvedSymbolError(sexp)
    # elif map
    # elif vector
    if (isinstance(sexp, SymbolicExpression)): # apply the symbolic expression
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
        elif "macro" == head.name:
            """In the end this should be replaced by a... macro"""
            ## Anonymous function ##
            ## returns a new closure ##
            argVector, body = sexp.positional[1], sexp.positional[2:]
            # what the closure should do is:
            # - gather all the free variables
            # - point to the local bindings in `bindings`
            bindings = env # this is temporary: 
            # for now, the entire enclosing scope in referenced. This may impair garbage collection too much.
            # in the future, the bindings will be only the ones references in the closure
            return Function(argVector, body, bindings, loaded_namespaces, is_macro=True)
        elif "do" == head.name:
            # do should create a new lexical environment
            last = None
            for exp in sexp.positional[1:]:
                last = ns_eval_sexp(exp, env, loaded_namespaces)
            return last
        elif "comment" == head.name:
            return None
        elif "let" == head.name:
            # I should remove the let
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
        elif "require" == head.name:
            # MAYBE THE NAMESPACE SHOULD ALWAYS HAVE ITSELF AS A PARENT NAMESPACE? THIS WAY I RESOLVE THE SELF-QUALIFYING PROBLEM
            ns_name = sexp.positional[1].name
            if ns_name not in loaded_namespaces:
                # creates a new environment for the new namespace
                ns_env = SimbaEnvironment(names = repl_env)
                # evaluates the content of that namespace in the new environment
                ns_eval_sexp(helpers.find_ns(ns_name, ast), ns_env, loaded_namespaces)
                # add the new namespace environment to the list of loaded namespaces
                loaded_namespaces[ns_name] = ns_env
                # add the environment to the list of contextual namespaces
                env.require_ns(ns_name, loaded_namespaces[ns_name])
            else:
                env.require_ns(ns_name, loaded_namespaces[ns_name])
        elif "include" == head.name:
            ns_name = sexp.positional[1].name
            if ns_name not in loaded_namespaces:
                # creates a new environment for the new namespace
                ns_env = SimbaEnvironment(names = repl_env)
                # evaluates the content of that namespace in the new environment
                ns_eval_sexp(helpers.find_ns(ns_name, ast), ns_env, loaded_namespaces)
                # add the new namespace environment to the list of loaded namespaces
                loaded_namespaces[ns_name] = ns_env
                # add the environment to the list of contextual namespaces
                env.include_ns(ns_name, loaded_namespaces[ns_name])
            else:
                env.include_ns(ns_name, loaded_namespaces[ns_name])
        elif "quasiquote" == head.name:
            # print_sexp(quasiquote(sexp[1]))
            return ns_eval_sexp(quasiquote(sexp[1]), env, loaded_namespaces)
        elif "macroexpand" == head.name:
            return macroexpand(sexp[1], env)
        else:
            ## Non-Special Forms ##
            ## evaluate the args ##
            evaledPArgs = [ns_eval_sexp(e, env, loaded_namespaces) for e in sexp.positional]
            evaledRArgs = {ns_eval_sexp(key, env, loaded_namespaces): ns_eval_sexp(value, env, loaded_namespaces) for key, value in sexp.relational}
            ## apply the head ##
            return evaledPArgs[0](*evaledPArgs[1:], **evaledRArgs)
    else: # if the value is an atomic data type, cannot evaluate further
        return sexp


def namespaced_eval(ast_list, run_tests = False, main_namespace = "main"):
    """Adds namespace functionality to the Simba evaluation.
    
    Keeps track of multiple namespaces in the namespaces variable.
    At any given time, a namespace is 'current', the current namespace is held in the ns variable. This is inspired by common lisp.
    
    The evaluation starts in the 'main' namespace. Every time a namespace is referred, that namespace the function looks for it in its
    AST representation of the program, and evaluates it if it is the first time it is referred."""
    # base_env = SimbaEnvironment(names = repl_env)
    # # evaluate the base namespace
    # ns_eval_sexp(, base_env, loaded_namespaces={})
    if run_tests:
        # get the test namespaces
        test_ns_list = helpers.find_test_ns(ast_list)
        # run them
        # print(test_ns_list)
        for ns in test_ns_list:
            ns_eval_sexp(ns, SimbaEnvironment(names = repl_env))
        return
    main = helpers.find_ns(main_namespace, ast_list)
    res = ns_eval_sexp(main, SimbaEnvironment(names = repl_env))


# when called with no arguments, the command is a terminal repl
if __name__ == "__main__" and len(sys.argv) == 1:
    simba_repl()
# when called with the name of a file, will interpret that file
elif __name__ == "__main__" and len(sys.argv) > 1:
    parser = argparse.ArgumentParser(description="This is the Simba programming language tool.")
    parser.add_argument("files", metavar="FILES", nargs='*')
    parser.add_argument("--main", default="main", help="specify the namespace to start execution in (defaults to `main`)")
    parser.add_argument("--run-tests", action='store_const', const=True, default=False, help="execute the tests, that is all the namespaces whose name ends in `-test`")
    args = parser.parse_args()

    # if not (args.files.contains('libraries') or args.files.contains('libraries/base.sb')):
    #     args.files = args.files + ['libraries/base.sb']
    ast = helpers.read_files(_reader, args.files)
    res = namespaced_eval(ast, args.run_tests, args.main)