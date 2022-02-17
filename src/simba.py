#! python3
import sys, traceback
from types import ModuleType
from typing import Tuple, Union

from prompt_toolkit.shortcuts.prompt import PromptSession
from prompt_toolkit.history import FileHistory

sys.path.insert(0, '.')

# import antlr4
import sexprs_reader_printer
import dotexprs_reader_printer
from simba_types import *
from simba_exceptions import MultipleDispatchException
import helpers

# command-line
import argparse

# _reader    = sexprs_reader_printer.SexpReader
# _read_form  = sexprs_reader_printer.read_str
# _print_ast = sexprs_reader_printer.to_string
_reader = sexprs_reader_printer

default_syntax = sexprs_reader_printer

def read_sexp(string, syntax = default_syntax): # returns a SymbolicExpression
    # read the frontmatter
    return syntax.read_str(string)

def bind_fn_args(fn_args:tuple, p_args: tuple, r_args: dict) -> dict:
    names = {}
    for i, arg in enumerate(fn_args):
        if arg.name == '&':
            names[fn_args[i+1].name] = p_args[i:]
            break
        else:
            names[arg.name] = p_args[i]
    return names

class Function:
    """Functions are anonymous, but may contain names in their metadata.
    Any Function can be promoted to a multimethod with the `register` method.
    """
    def __init__(self, params, ast, bindings, loaded_ns, r_args = {}):
        # if len(params) < 1 or params[0] != Symbol('vector'): raise SyntaxError("Function declaration was expecting a vector as the first argument.")
        # if r_args: print(r_args)
        # positonalParams = pass
        # namedParams = pass
        self.args = params
        self.ast = ast
        self.guard = None if 'guard' not in r_args else r_args['guard']
        self.bindings = bindings # the bindings should hold the bindings from the args and closure
        self.loaded_ns = loaded_ns
        self.macro = r_args['macro'] if 'macro' in r_args else False
        if 'meta' in r_args:
            self.meta = r_args['meta']
        else:
            self.meta = {}
        for k in ['macro', 'meta']:
            if k in r_args: r_args.pop(k)
        self.meta = self.meta | r_args
    def register(self, fn):
        return Multi(self, **self.meta, macro = self.macro).register(fn) # add meta
    def __call__(self, *e_p_args, **e_r_args):
        # a fn should have no dynamically bound symbols in it.
        # Its environment consists in the args + enclosed free variables at the time of creation
        res =  None
        env = SimbaEnvironment(
                outer=self.bindings,
                names=bind_fn_args(self.args, e_p_args, e_r_args)
            )
        for e in self.ast:
            # evaluate in an implicit do #
            res = eval_sexp(e, env = env, loaded_namespaces=self.loaded_ns)
        return res

def check_guard(guard:Union[Function,None], p_args:tuple, r_args:dict):
    if guard:
        return guard(*p_args, **r_args)
    else:
        return True

def signature_match(signature:tuple, p_args:tuple, r_args:dict, guard: Union[Function,None] = None) -> bool:
    if Symbol('&') in signature:
        return check_guard(guard, p_args, r_args) and True
    else:
        # TODO: for now the signature length does not take into account the keyword arguments or type signatures
        return len(p_args) == len(signature) and check_guard(guard, p_args, r_args)

class Multi:
    """All functions can be promoted to multimethods.
    """
    def __init__(self, fn:Function, **meta):
        self.method_table: List[Tuple[Tuple, Function, Union[Function, None]]] = []
        self.meta = meta
        if 'macro' in self.meta:
            self.macro = self.meta['macro']
            self.meta.pop('macro')
        else: 
            self.macro = False
        self.register(fn)
    def register(self, fn: Function):
        self.method_table.append((fn.args, fn, fn.guard))
        return self
    def clear(self):
        self.method_table = []
    def signatures(self):
        r = []
        for t in self.method_table:
            r.append((t[0], t[2]))
        return r
    def __len__(self):
        return len(self.method_table)
    def __call__(self, *p_args, **r_args):
        for tup in self.method_table:
            if signature_match(tup[0], p_args, r_args, guard = tup[2]):
                return tup[1](*p_args, **r_args)
        n = self.meta['name'] if 'name' in self.meta else ""
        raise MultipleDispatchException(f"No matching signature for multimethod {n}")

def print_sexp(sexp, syntax = default_syntax, lb=False) -> str:
    return syntax.to_string(sexp, lb=lb)

from base_functions import repl_env

def convert(string, _from, to):
    return to.print_sexp(_from.read_sexp(string))

# def simba_import(module):
#     importlib.import_module(module)

# def eval_form(env, form, print_result = False):
#     result = eval_sexp(form, env)
#     if print_result: print(print_sexp(result))

def simba_repl(multi = False):
    eof = False
    _env = SimbaEnvironment(names = repl_env)
    loaded = {}
    session = PromptSession(FileHistory('~/.simba_history'))
    # load the standard libraries
    eval_sexp(helpers.read_files(_reader, ['standard']), _env, loaded)
    def eval_util(e):
        res = eval_sexp(e, _env, loaded)
        print(print_sexp(res))
    while not eof:
        try:
            line = session.prompt('>>> ', multiline=multi)
            helpers.read_string_form_by_form(
                _reader,
                eval_util,
                line
            )
        except EOFError:
            eof = True
        except KeyboardInterrupt:
            print('Exit with Ctrl-D')
            eof = True
        except Exception as e:
            print("".join(traceback.format_exception(*sys.exc_info())))

def quasiquote(ast):
    """The quasiquote expansion algorithm"""
    if isinstance(ast, Symbol) or isinstance(ast, Map): 
        return SymbolicExpression(Symbol('quote'), ast)
    # if isinstance(ast, Keyword):
    #     return SymbolicExpression(Symbol('quote'), )
    elif isinstance(ast, SymbolicExpression) and ast[0] == Symbol("unquote"):
        return ast[1]
    elif isinstance(ast, SymbolicExpression):
        relational = []
        for k in ast.relational:
            relational.append(Keyword(k)); relational.append(ast.relational[k])
        res = SymbolicExpression()
        for e in helpers.reverse(ast.positional):
            if isinstance(e, SymbolicExpression) and e[0] == Symbol("splice-unquote"):
                res = SymbolicExpression(Symbol('concat'), e[1], res)
            else:
                res = SymbolicExpression(Symbol('prepend-sexp'), quasiquote(e), res)
        # TODO: DOES THIS ALGORITHM PERFORM MACROEXPANSION ON KEYWORD ARGUMENTS??
        res = SymbolicExpression(Symbol('concat'), res, relational)
        return res
    else:
        return ast

def is_macro_call(ast, env):
    if isinstance(ast, SymbolicExpression) and len(ast.positional) != 0 and isinstance(ast[0], Symbol):
        try:
            refers_to = env.get(ast[0])
        except:
            refers_to = None
        if isinstance(refers_to, Function) and refers_to.macro == True:
            return True
    return False

def macroexpand(ast, env):
    """This is the most basic macroexpansion algorithm possible:
    While the head of the expression resolves to a macro, the corresponding
    macro function is called on its **unevaluated** arguments.

    Further improvements to this algorithm could be automatically namespaced
    symbols or autogensyms.
    """
    while is_macro_call(ast, env):
        # print(ast[0])
        macro_fn = env.get(ast[0])
        p_args = ast[1:]
        r_args = ast.relational
        ast = macro_fn(*p_args, **r_args)
        # print(ast)
    return ast

def eval_primitive(sexp, env, loaded_namespaces):
    """This function is charged of evaluating anything that is not a SymbolicExpression.
    In other words it just returns primitive data structures like Symbols, Vectors, etc...
    This distinction is made so that it is feasible to implement Tail Call Optimization
    on Symbolic Expression evaluation.
    """
    if isinstance(sexp, Symbol): # if symbol evaluate to its binding
        # here if symbol is qualified with module name return (get-attr "f" module)
        if sexp.namespace:
            if sexp.namespace == "py":
                return eval(sexp.name)
            resolution = env.get(Symbol(sexp.namespace))
            if isinstance(resolution , ModuleType):
                return getattr(resolution, sexp.name)
        try: return env.get(sexp)
        except KeyError: raise UnresolvedSymbolError(sexp)
    elif isinstance(sexp, Vector):
        return [eval_sexp(e, env, loaded_namespaces) for e in sexp]
    elif isinstance(sexp, Map):
        return {eval_sexp(key, env, loaded_namespaces): eval_sexp(sexp[key], env, loaded_namespaces) for key in sexp}
    else: # if the value is an atomic data type, cannot evaluate further
        return sexp

def eval_sexp(sexp, env, loaded_namespaces = {}):
    """
    `ns_eval_exp` evaluates a Symbolic Expression within a context.
    The context is the 'environment' a mapping of names to namespaces,
    and the namespace in which the execution is working at the moment.
    By default, execution starts in the `None` namespace, which corresponds to the standard library.
    """
    # print(print_sexp(sexp))
    while True:
        if not isinstance(sexp, SymbolicExpression):
            return eval_primitive(sexp, env, loaded_namespaces)

        # macroexpansion step
        sexp = macroexpand(sexp, env)

        # We need to check for primitive datatypes before and after macroexpansion unfortunately
        if not isinstance(sexp, SymbolicExpression):
            return eval_primitive(sexp, env, loaded_namespaces)

        if len(sexp.positional) == 0:
            return None
        ## Special Forms: ##
        # if isinstance(head := sexp.positional[0], SymbolicExpression):
        #     evaledPArgs = [eval_sexp(e, env, loaded_namespaces) for e in sexp.positional]
        #     evaledRArgs = {eval_sexp(key, env, loaded_namespaces): \
        #                         eval_sexp(sexp.relational[key], env, loaded_namespaces) \
        #                         for key in sexp.relational}
        #     return evaledPArgs[0](*evaledPArgs[1:], **evaledRArgs)
        head = sexp.positional[0]
        if "def" == head.name:
            ## def adds a binding (from unevaluated first arg to evaled second arg) in the environment ##
            if len(sexp.positional) < 3 and not isinstance(sexp.positional[1], Vector):
                raise SyntaxError("`def` statement has invalid argument pattern")
            a1 = sexp.positional[1]
            if isinstance(a1, list):
                for name, value in zip(a1[0::2], a1[1::2]):
                    res = eval_sexp(value, env, loaded_namespaces)
                    env.set(name, res)
                return None
            else:
                a2 = sexp.positional[2]
                res = eval_sexp(a2, env, loaded_namespaces)
                return env.set(a1, res)
        elif "quote" == head.name:
            if len(sexp.positional) != 2: raise Exception("`quote` expected 1 argument")
            return sexp.positional[1]
        elif "if" == head.name:
            # print("Going into if ")
            if len(sexp.positional) < 3:
                raise SyntaxError("Too few arguments to if")
            if len(sexp.positional) > 4:
                raise SyntaxError("Too many arguments to if")
            cond, then = sexp.positional[1:3]
            evaled_cond = eval_sexp(cond, env, loaded_namespaces)
            if evaled_cond:
                # return eval_sexp(then, env, loaded_namespaces)
                sexp = then 
                continue # TCO
            else:
                if (len(sexp.positional) == 4):
                    _else = sexp.positional[3]
                    # return eval_sexp(_else, env, loaded_namespaces)
                    sexp = _else 
                    continue # TCO
                else: return None
        elif "fn" == head.name:
            arg1 = sexp.positional[1]
            if isinstance(arg1, Vector):
                # anonymous function (single method declaration)
                argVector, body = sexp.positional[1], sexp.positional[2:]
                # what the closure should do is:
                # - gather all the free variables
                # - point to the local bindings in `bindings`
                bindings = env # this is temporary:
                # for now, the entire enclosing scope in referenced. This may impair garbage collection too much.
                # in the future, the bindings will be only the ones references in the closure
                return Function(argVector, body, bindings, loaded_namespaces, sexp.relational)
            elif isinstance(arg1, SymbolicExpression):
                # anonymous multimethod (with multiple method declarations)
                fn = Function(sexp[1][0], sexp[1][1:], env, loaded_namespaces, sexp.relational)
                for exp in sexp[2:]:
                    # argVector, body = exp.positional[0], exp.positional[1:]
                    fn = fn.register(Function(exp.positional[0], exp.positional[1:], env, loaded_namespaces, sexp.relational))
                return fn
        elif "do" == head.name:
            # TODO: add scope to the do
            if len(sexp.positional) == 1: return None
            eval_sexp(sexp[1:-1], env, loaded_namespaces)
            sexp = sexp[-1]
            continue # TCO
        # elif "let" == head.name:
        #     # I should remove the let
        #     ## creates a new environment and binds the values to it successively (in order) ##
        #     vec, body = sexp.positional[1], sexp.positional[2:]
        #     let_env = SimbaEnvironment(outer = env)
        #     for i in range(0, len(vec), 2):
        #         let_env.set(vec[i], eval_sexp(vec[i+1], let_env, loaded_namespaces))
        #     ## evaluate the body in an implicit do ##
        #     last = None
        #     for exp in body:
        #         last = eval_sexp(exp, let_env, loaded_namespaces)
        #     return last
        elif "try" == head.name:
            if Keyword('catch') in sexp and Keyword('finally') in sexp:
                try:
                    res = None
                    for exp in sexp[1:]:
                        res = eval_sexp(exp, env, loaded_namespaces)
                    return res
                except:
                    return eval_sexp(sexp['catch'], env, loaded_namespaces)
                finally:
                    eval_sexp(sexp['finally'], env, loaded_namespaces)
            elif Keyword('catch') in sexp:
                try:
                    res = None
                    for exp in sexp[1:]:
                        res = eval_sexp(exp, env, loaded_namespaces)
                    return res
                except:
                    return eval_sexp(sexp['catch'], env, loaded_namespaces)
            elif Keyword('finally') in sexp:
                try:
                    res = None
                    for exp in sexp[1:]:
                        res = eval_sexp(exp, env, loaded_namespaces)
                    return res
                finally:
                    eval_sexp(sexp['finally'], env, loaded_namespaces)
            else:
                res = None
                for exp in sexp[1:]:
                    res = eval_sexp(exp, env, loaded_namespaces)
                return res
        elif "ns" == head.name:
            # 1. Initialize the namespace and add it to the namespaces
            # 2. Jump into the namespace to start evaluation
            last = None
            for exp in sexp.positional[2:]:
                last = eval_sexp(exp, env, loaded_namespaces)
            return last
        elif "require" == head.name:
            # MAYBE THE NAMESPACE SHOULD ALWAYS HAVE ITSELF AS A PARENT NAMESPACE? THIS WAY I RESOLVE THE SELF-QUALIFYING PROBLEM
            ns_name = sexp.positional[1].name
            if ns_name not in loaded_namespaces:
                # creates a new environment for the new namespace
                ns_env = SimbaEnvironment(names = repl_env)
                # evaluates the content of that namespace in the new environment
                eval_sexp(helpers.find_ns(ns_name, program_ast), ns_env, loaded_namespaces)
                # add the new namespace environment to the list of loaded namespaces
                loaded_namespaces[ns_name] = ns_env
                # add the environment to the list of contextual namespaces
                env.require_ns(ns_name, loaded_namespaces[ns_name])
            else:
                env.require_ns(ns_name, loaded_namespaces[ns_name])
        elif "include" == head.name:
            # print("Including")
            ns_name = sexp.positional[1].name
            if ns_name not in loaded_namespaces:
                # creates a new environment for the new namespace
                ns_env = SimbaEnvironment(names = repl_env)
                # evaluates the content of that namespace in the new environment
                eval_sexp(helpers.find_ns(ns_name, program_ast), ns_env, loaded_namespaces)
                # add the new namespace environment to the list of loaded namespaces
                loaded_namespaces[ns_name] = ns_env
                # add the environment to the list of contextual namespaces
                env.include_ns(ns_name, loaded_namespaces[ns_name])
                break
            else:
                env.include_ns(ns_name, loaded_namespaces[ns_name])
                # print("made it second")
                break
        elif "quasiquote" == head.name:
            # print(sexp)
            # print(print_sexp(quasiquote(sexp[1])))
            # return eval_sexp(quasiquote(sexp[1]), env, loaded_namespaces)
            sexp = quasiquote(sexp[1])
            continue # TCO
        elif "macroexpand" == head.name:
            if len(sexp.positional) != 2: return Exception("`macroexpand` expected 1 argument.")
            return macroexpand(sexp[1], env)
        else:
            ## Non-Special Forms ##
            ## evaluate the args ##
            evaledPArgs = [eval_sexp(e, env, loaded_namespaces) for e in sexp.positional]
            evaledRArgs = {eval_sexp(key, env, loaded_namespaces): \
                            eval_sexp(sexp.relational[key], env, loaded_namespaces) \
                            for key in sexp.relational}
            if isinstance(fun := evaledPArgs[0], Function): # or isinstance(head, Multi):
                # print("Yoohoo")
                # print (bind_fn_args(fun.args, evaledPArgs[1:], evaledRArgs))
                env = SimbaEnvironment(
                    outer = fun.bindings,
                    names = bind_fn_args(fun.args, evaledPArgs[1:], evaledRArgs) # args are the names of the env
                )
                for e in fun.ast[:-1]: eval_sexp(e, env, loaded_namespaces)
                sexp = fun.ast[-1]
                continue
            else:
                ## apply the head ##
                return evaledPArgs[0](*evaledPArgs[1:], **evaledRArgs)


def namespaced_eval(ast_list, run_tests = False, main_namespace = "main"):
    """Adds namespace functionality to the Simba evaluation.
    
    Keeps track of multiple namespaces in the namespaces variable.
    At any given time, a namespace is 'current', the current namespace is held in the ns variable. This is inspired by common lisp.
    
    The evaluation starts in the 'main' namespace. Every time a namespace is referred, that namespace the function looks for it in its
    AST representation of the program, and evaluates it if it is the first time it is referred."""
    # base_env = SimbaEnvironment(names = repl_env)
    # # evaluate the base namespace
    # eval_sexp(, base_env, loaded_namespaces={})
    if run_tests:
        # get the test namespaces
        test_ns_list = helpers.find_test_ns(ast_list)
        # run them
        # print(test_ns_list)
        for ns in test_ns_list:
            eval_sexp(ns, SimbaEnvironment(names = repl_env))
        return
    main = helpers.find_ns(main_namespace, ast_list)
    res = eval_sexp(main, SimbaEnvironment(names = repl_env))


# when called with no arguments, the command is a terminal repl
if __name__ == "__main__" and len(sys.argv) == 1:
    simba_repl()
# when called with the name of a file, will interpret that file
elif __name__ == "__main__" and len(sys.argv) > 1:
    parser = argparse.ArgumentParser(description="This is the Simba programming language tool. Call without arguments to start a command line repl, else the arguments specify the files to execute. At the REPL, press ALT+ENTER to submit.")
    parser.add_argument("files", metavar="FILES", nargs='*')
    parser.add_argument("--main", default="main", help="specify the namespace to start execution in (defaults to `main`)")
    parser.add_argument("--run-tests", action='store_const', const=True, default=False, help="execute the tests, that is all the namespaces whose name ends in `-test`")
    args = parser.parse_args()

    # if not (args.files.contains('libraries') or args.files.contains('libraries/base.sb')):
    #     args.files = args.files + ['libraries/base.sb']
    program_ast = helpers.read_files(_reader, args.files) # + helpers.read_files(_reader, ['standard'])
    # print(print_sexp(ast))
    res = namespaced_eval(program_ast, args.run_tests, args.main)