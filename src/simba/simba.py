#! python3
import sys, traceback
from types import ModuleType
from typing import Tuple, Union
from importlib.resources import read_text

import argparse
from prompt_toolkit.shortcuts.prompt import PromptSession
from prompt_toolkit.history import FileHistory

import pyrsistent as p

sys.path.insert(0, '.')

# import antlr4
import sexprs_reader_printer
import dotexprs_reader_printer
from simba_types import *
import helpers
import sb

# _reader    = sexprs_reader_printer.SexpReader
# _read_form  = sexprs_reader_printer.read_str
# _print_ast = sexprs_reader_printer.to_string
_reader = sexprs_reader_printer

default_syntax = sexprs_reader_printer

# def read_sexp(string, syntax = default_syntax): # returns a SymbolicExpression
#     # read the frontmatter
#     return syntax.read_str(string)

def read_string(string):
    """Returns the first object from the string."""
    return _reader.SexpReader(string).read_form()

def print_sexp(sexp, syntax = default_syntax, lb=False) -> str:
    return syntax.to_string(sexp, lb=lb)

from simba_exceptions import SimbaException, MultipleDispatchException, FailingGuardException, MultiMethodException, SimbaSyntaxError

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
    def __init__(self, params, ast, bindings, _r_args = None):
        # positonalParams = pass
        # namedParams = pass
        r_args = _r_args if _r_args is not None else {}
        self.args = params
        self.ast = ast
        self.guard = None if 'when' not in r_args else r_args['when']
        self.bindings = bindings # the bindings should hold the bindings from the args and closure
        self.macro = r_args['macro'] if 'macro' in r_args else False
        self.method_table = []
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
        res =  None
        env = Environment(
                outer=self.bindings,
                names=bind_fn_args(self.args, e_p_args, e_r_args)
            )
        for e in self.ast:
            res = eval_sexp(e, env = env)
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

class MultiFn():
    """A multimethod. Dispatch is made according to the result of the dispatching function."""
    def __init__(self, name, dispatch_fn):
        self.name = name
        self.dispatch_fn = dispatch_fn
        self.method_table = {} # a mapping of dispatch-value to functions
    def __len__(self):
        return len(self.method_table)
    def register(self, fn, dispatch_value):
        if dispatch_value in self.method_table:
            raise MultiMethodException(f"The dispatch value {print_sexp(dispatch_value)} is already registered for the multimethod {self.name}.")
        self.method_table[dispatch_value] = fn
    def methods(self):
        """Returns a list of the registered dispatch values on the multimethod."""
        return p.pvector(self.method_table.keys())
    # def __call__(self):
    #     dispatch_val = self.dispatch_fn()
    #     # if val not in dict dispatch to the default fn?
    #     return self.method_table[dispatch_val]()

def convert(string, _from, to):
    return to.print_sexp(_from.read_sexp(string))

# def eval_form(env, form, print_result = False):
#     result = eval_sexp(form, env)
#     if print_result: print(print_sexp(result))

def simba_repl(multi = False):
    """Command-line repl that executes everything in the base namespace by default."""
    eof = False
    prompt_session = PromptSession(FileHistory('~/.simba_history'))
    # load the standard library
    _env = Namespace()
    eval_sexp(SymbolicExpression(Symbol('ns'), Symbol('repl')), _env)
    while not eof:
        try:
            line = prompt_session.prompt('>>> ', multiline=multi)
            readerObj = _reader.SexpReader(line)
            while readerObj.position < len(readerObj.tokens):
                e = readerObj.read_form()
                res = eval_sexp(e, _env)
                print(print_sexp(res))
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
        macro_fn = env.get(ast[0])
        p_args = ast[1:]
        r_args = ast.relational
        ast = macro_fn(*p_args, **r_args)
    return ast

loaded_ns = {}

def require(ns_names, env, include = False):
    """Side effecting function that requires a namespace such that it is accessible in the current namespace (if namespace-qualified)."""
    global loaded_ns
    for n in ns_names:
        if n not in loaded_ns:
            env_cache = env
            # creates a new environment for the new namespace
            ns_env = Namespace(name = n)
            # evaluates the content of that namespace in the new environment
            # here the ns form will change the *ns*
            for exp in helpers.return_ns(n, program_ast):
                eval_sexp(exp, ns_env)
            # add the new namespace environment to the list of loaded namespaces
            loaded_ns[n] = ns_env
            # add the environment to the list of contextual namespaces
            if include: env.include_ns(loaded_ns[n])
            else:       env.require_ns(loaded_ns[n])
            # here we must change the *ns* back
            env = env_cache
        else:
            if include: env.include_ns(loaded_ns[n])
            else:       env.require_ns(loaded_ns[n])

def eval_primitive(sexp, env):
    """This function is charged of evaluating anything that is not a SymbolicExpression.
    In other words it just returns primitive data structures like Symbols, Vectors, etc...
    This distinction is made so that it is feasible to implement Tail Call Optimization
    on Symbolic Expression evaluation.
    """
    if isinstance(sexp, Symbol): # if symbol evaluate to its binding
        if sexp.name == "*ns*":
            return env.ns
        elif sexp.name == "*env*":
            return env
        if sexp.namespace:
            if sexp.namespace == "py":
                return eval(sexp.name)
            try:
                resolution = env.get(Symbol(sexp.namespace))
                if isinstance(resolution , ModuleType):
                    return getattr(resolution, sexp.name)
                # here it would be cleaner if a symba ns was the same as a python module, just a var in global scope
            except UnresolvedSymbolError:
                pass # do nothing
        try: return env.get(sexp)
        except KeyError: raise UnresolvedSymbolError(sexp)
    elif isinstance(sexp, Vector):
        return p.pvector([eval_sexp(e, env) for e in sexp])
    elif isinstance(sexp, Map):
        return p.pmap({eval_sexp(key, env): eval_sexp(sexp[key], env) for key in sexp})
    else: # if the value is an atomic data type, cannot evaluate further
        return sexp

def eval_sexp(sexp, env):
    """`eval_exp` evaluates a Symbolic Expression within a context.
    The context is the 'environment' a mapping of names to namespaces,
    and the namespace in which the execution is working at the moment.
    By default, execution starts in the `None` namespace, which corresponds to the standard library.
    """
    global loaded_ns
    while True:
        # print(sexp)
        if not isinstance(sexp, SymbolicExpression):
            return eval_primitive(sexp, env)

        # macroexpansion step
        sexp = macroexpand(sexp, env)

        # We need to check for primitive datatypes before and after macroexpansion unfortunately
        if not isinstance(sexp, SymbolicExpression):
            return eval_primitive(sexp, env)

        if len(sexp.positional) == 0:
            return None
        ## Special Forms: ##
        if isinstance(head := sexp.positional[0], SymbolicExpression):
            head = sexp.positional[0] = eval_sexp(head, env)
        head = sexp.positional[0]
        is_s = isinstance(head, Symbol)
        if is_s and "def" == head.name:
            if len(sexp.positional) < 3:
                raise SimbaSyntaxError(f"\n\t`def` statement has invalid argument pattern in:\n\t{print_sexp(sexp)}")
            _name = sexp.positional[1]
            _val = sexp.positional[2]
            _res = eval_sexp(_val, env)
            return env.ns.set(_name, _res)
        elif is_s and "quote" == head.name:
            if len(sexp.positional) != 2: raise SimbaSyntaxError(f"\n\t`quote` expected 1 argument in:\n\t{print_sexp(sexp)}")
            return sexp.positional[1]
        elif is_s and "if" == head.name:
            if len(sexp.positional) < 3:
                raise SimbaSyntaxError(f"\n\tToo few arguments to if in:\n\t{print_sexp(sexp)}")
            if len(sexp.positional) > 4:
                raise SimbaSyntaxError(f"\n\tToo many arguments to if in:\n\t{print_sexp(sexp)}")
            cond, then = sexp.positional[1:3]
            evaled_cond = eval_sexp(cond, env)
            if evaled_cond:
                sexp = then 
                continue # TCO
            else:
                if (len(sexp.positional) == 4):
                    _else = sexp.positional[3]
                    sexp = _else 
                    continue # TCO
                else: return None
        elif is_s and "fn" == head.name:
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
                return Function(argVector, body, bindings, sexp.relational)
            elif isinstance(arg1, SymbolicExpression):
                # anonymous multimethod (with multiple method declarations)
                fn = Function(sexp[1][0], sexp[1][1:], env, sexp.relational)
                for exp in sexp[2:]:
                    # argVector, body = exp.positional[0], exp.positional[1:]
                    fn = fn.register(Function(exp.positional[0], exp.positional[1:], env, sexp.relational))
                return fn
        elif is_s and "do" == head.name:
            if len(sexp.positional) == 1: return None
            for e in sexp[1:-1]:
                eval_sexp(e, env)
            sexp = sexp[-1]
            continue # TCO
        elif is_s and "let" == head.name:
            # creates a new environment and binds the values to it successively (in order)
            # evaluates the body in an implicit do
            if len(sexp.positional) == 2: raise SimbaSyntaxError(f"\n\t`let` form is missing a body in:\n\t{print_sexp(sexp)}")
            vec = sexp.positional[1]
            env = Environment(outer = env)
            for i in range(0, len(vec), 2):
                env.set(vec[i], eval_sexp(vec[i+1], env))
            for exp in sexp[2:-1]:
                eval_sexp(exp, env)
            sexp = sexp[-1]
            continue # TCO
        elif is_s and "try" == head.name:
            if Keyword('catch') in sexp and Keyword('finally') in sexp:
                try:
                    res = None
                    for exp in sexp[1:]:
                        res = eval_sexp(exp, env)
                    return res
                except:
                    return eval_sexp(sexp['catch'], env)
                finally:
                    eval_sexp(sexp['finally'], env)
            elif Keyword('catch') in sexp:
                try:
                    res = None
                    for exp in sexp[1:]:
                        res = eval_sexp(exp, env)
                    return res
                except:
                    return eval_sexp(sexp['catch'], env)
            elif Keyword('finally') in sexp:
                try:
                    res = None
                    for exp in sexp[1:]:
                        res = eval_sexp(exp, env)
                    return res
                finally:
                    eval_sexp(sexp['finally'], env)
            else:
                res = None
                for exp in sexp[1:]:
                    res = eval_sexp(exp, env)
                return res
        elif is_s and "ns" == head.name:
            ns_name = sexp.positional[1].name                
            if ns_name not in loaded_ns:
                if env.ns.name == "":
                    # it means the execution is not currently happening in an environment:
                    # reuse the empty shell of an env here
                    env.ns.name = ns_name
                else:
                    # create new Namespace if it does not yet exist
                    env = Namespace(name = ns_name)
                # add it to the list of loaded namespaces
                loaded_ns[ns_name] = env
            # includes the base library and imports all classes from java.lang
            require(['base'], env.ns, include = True)
            # requires/refers other namespaces and vars as specified
            # dadi
            break
        elif is_s and "require" == head.name:
            require([sexp.positional[1].name], env.ns)
            break
        elif is_s and "include" == head.name:
            require([sexp.positional[1].name], env.ns, include=True)
            break
        elif is_s and "quasiquote" == head.name:
            sexp = quasiquote(sexp[1])
            continue # TCO
        elif is_s and "macroexpand" == head.name:
            if len(sexp.positional) != 2: return Exception("`macroexpand` expected 1 argument.")
            return macroexpand(sexp[1], env)
        else:
            ## Non-Special Forms ##
            ## evaluate the args ##
            evaledPArgs = [eval_sexp(e, env) for e in sexp.positional]
            evaledRArgs = {eval_sexp(key, env): \
                            eval_sexp(sexp.relational[key], env) \
                            for key in sexp.relational}
            matched = False
            if isinstance(fun := evaledPArgs[0], Multi):
                for tup in fun.method_table:
                    if signature_match(tup[0], evaledPArgs[1:], evaledRArgs, guard = tup[2]):
                        fun = evaledPArgs[0] = tup[1]
                        matched = True
                        break
                if not matched: raise MultipleDispatchException(f"No matching signature {evaledPArgs} for multimethod {sexp[0].name}")
            if isinstance(fun, MultiFn):
                # evaluate the dispatch function
                val = eval_sexp(SymbolicExpression(fun.dispatch_fn, *evaledPArgs[1:], **evaledRArgs), env)
                # if the value is missing from the dispatch table fall back to "default"
                if val not in fun.method_table:
                    try:
                        fun = fun.method_table["default"]
                    except KeyError:
                        raise MultipleDispatchException(f"Tried to fall back to the default method but no such method exists for {fun.name}.")
                else:
                    fun = fun.method_table[val]
            if isinstance(fun, Function):
                env = Environment(
                    outer = fun.bindings,
                    names = bind_fn_args(fun.args, evaledPArgs[1:], evaledRArgs) # args are the names of the env
                )
                # first check the guard if there is a guard and the fn has not already been selected from a multi
                if fun.guard and not matched and not eval_sexp(fun.guard, env):
                    raise FailingGuardException('The guard condition is failing for the function.')
                # if the body is empty return `nil`
                if len(fun.ast) == 0:
                    return None
                for e in fun.ast[:-1]: eval_sexp(e, env)
                sexp = fun.ast[-1]
                continue
            else:
                ## apply the head ##
                return fun(*evaledPArgs[1:], **evaledRArgs)


def namespaced_eval(ast_list, run_tests = False, main_namespace = "main"):
    """Adds namespace functionality to the Simba evaluation.
    
    Keeps track of multiple namespaces in the namespaces variable.
    At any given time, a namespace is 'current', the current namespace is held in the ns variable. This is inspired by common lisp.
    
    The evaluation starts in the 'main' namespace. Every time a namespace is referred, that namespace the function looks for it in its
    AST representation of the program, and evaluates it if it is the first time it is referred."""
    if run_tests:
        # get the test namespaces
        test_ns_list = helpers.return_test_ns(ast_list)
        # run them
        for ns in test_ns_list:
            env = Namespace()
            for e in ns:
                eval_sexp(e, env)
        return
    main = helpers.return_ns(main_namespace, ast_list)
    env = Namespace()
    for e in main:
        eval_sexp(e, env)

def main():
    """Serves as an entrypoint for the script."""
    global program_ast
    base_lib = read_text(sb, 'base.sb')
    # when called with no arguments, the command is a terminal repl
    if len(sys.argv) == 1:
        program_ast = helpers.read_string_eager(base_lib)
        simba_repl()
    # when called with the name of a file, will interpret that file
    elif len(sys.argv) > 1:
        parser = argparse.ArgumentParser(description="This is the Simba programming language tool. Call without arguments to start a command line repl, else the arguments specify the files to execute. At the REPL, press ALT+ENTER to submit.")
        parser.add_argument("files", metavar="FILES", nargs='*')
        parser.add_argument("--main", default="main", help="specify the namespace to start execution in (defaults to `main`)")
        parser.add_argument("--run-tests", action='store_const', const=True, default=False, help="execute the tests, that is all the namespaces whose name ends in `-test`")
        args = parser.parse_args()

        program_ast = helpers.read_files(_reader, args.files) + helpers.read_string_eager(base_lib)
        namespaced_eval(program_ast, args.run_tests, args.main)

if __name__ == "__main__":
    main()