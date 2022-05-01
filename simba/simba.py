#! python3
import sys, traceback
from types import ModuleType, LambdaType
from typing import Tuple, Union
from importlib.resources import read_text
import traceback

import argparse
from prompt_toolkit.shortcuts.prompt import PromptSession
from prompt_toolkit.history import FileHistory

import pyrsistent as p

# import antlr4
import simba.sexprs_reader_printer as sexprs_reader_printer
# import src.simba.dotexprs_reader_printer
from simba.lang.types import PersistentVector, Symbol, PersistentMap, PersistentVector, Namespace, Environment, Keyword, Var
from simba.lang.PersistentList import PersistentList
import simba.helpers as helpers
import simba.sb as sb

# _reader    = sexprs_reader_printer.SexpReader
# _read_form  = sexprs_reader_printer.read_str
# _print_ast = sexprs_reader_printer.to_string
_reader = sexprs_reader_printer

default_syntax = sexprs_reader_printer

# def read_sexp(string, syntax = default_syntax): # returns a PersistentList
#     # read the frontmatter
#     return syntax.read_str(string)

def read_string(string):
    """Returns the first object from the string."""
    return _reader.SexpReader(string).read_form()

def print_sexp(sexp, syntax = default_syntax, lb=False) -> str:
    return syntax.to_string(sexp, lb=lb)

from simba.exceptions import IllegalStateException, SimbaException, MultipleDispatchException, MultiMethodException, SimbaSyntaxError, UnresolvedSymbolError

def bind_fn_args(fn_args, _args, recur = False) -> dict:
    # print(fn_args)
    # print(_args)
    names = {}
    for i, arg in enumerate(fn_args):
        if arg.name == '&':
            if not recur:
                names[fn_args[i+1].name] = _args[i:]
            else:
                names[fn_args[i+1].name] = _args[i]
            break
        else:
            names[arg.name] = _args[i]
    return names

class Function:
    """Functions are anonymous, but may contain names in their metadata.
    Any Function can be promoted to a multimethod with the `register` method.
    """
    def __init__(self, params, ast, bindings, optname = None, optmap = None):
        self.args = params
        self.ast = ast
        self.bindings = bindings # the bindings should hold the bindings from the args and closure
        self.name = optname
        self.optmap = optmap
    def register(self, fn):
        return OverloadedFn(self).register(fn) # add meta
    def __call__(self, *e_p_args):
        res =  None
        env = Environment(
                outer=self.bindings,
                names=bind_fn_args(self.args, e_p_args)
            )
        for e in self.ast:
            res = eval_sexp(e, env = env)
        return res

def signature_match(signature:tuple, args:tuple):
    return True if Symbol('&') in signature else len(args) == len(signature)

class OverloadedFn:
    """Not to be confused with a MultiFn, this is the type that allows for variadic dispatch."""
    def __init__(self, fn:Function):
        self.method_table: PersistentList[Tuple[Tuple, Function]] = []
        self.register(fn)
    def register(self, fn: Function):
        self.method_table.append((fn.args, fn))
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
            if signature_match(tup[0], p_args):
                return tup[1](*p_args, **r_args)
        raise MultipleDispatchException("No matching signature for multimethod")

class MultiFn:
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
        return PersistentVector.create(self.method_table.keys())
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
    eval_sexp(PersistentList.create(Symbol('ns'), Symbol('repl')), _env)
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
    if isinstance(ast, Symbol) or isinstance(ast, PersistentMap): 
        return PersistentList.create(Symbol('quote'), ast)
    elif isinstance(ast, PersistentList) and ast[0] == Symbol("unquote"):
        return ast[1]
    elif isinstance(ast, PersistentList):
        res = PersistentList.create()
        for e in helpers.reverse(ast):
            if isinstance(e, PersistentList) and e[0] == Symbol("splice-unquote"):
                res = PersistentList.create(Symbol('concat'), e[1], res)
            else:
                res = PersistentList.create(Symbol('cons'), quasiquote(e), res)
        res = PersistentList.create(Symbol('concat'), res) 
        return res
    else:
        return ast

def is_macro_call(ast, env):
    if isinstance(ast, PersistentList) and len(ast) != 0 and isinstance(ast[0], Symbol):
        try:
            refers_to = env.get(ast[0], deref_var = False)
        except:
            refers_to = None
        if hasattr(refers_to, 'meta') and Keyword('macro') in refers_to.meta:
            return refers_to.meta[Keyword('macro')]
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
        ast = eval_sexp(PersistentList.create(macro_fn, *p_args), env, macro_call = True)
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
    """This function is charged of evaluating anything that is not a PersistentList.
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
            try:
                resolution = env.get(Symbol(sexp.namespace))
                if isinstance(resolution , ModuleType) or isinstance(resolution, type):
                    return getattr(resolution, sexp.name)
                # here it would be cleaner if a symba ns was the same as a python module, just a var in global scope
            except UnresolvedSymbolError:
                pass # do nothing
        try:
            return env.get(sexp)
        except KeyError:
            raise UnresolvedSymbolError(sexp)
    elif isinstance(sexp, PersistentVector):
        return PersistentVector.create([eval_sexp(e, env) for e in sexp])
    elif isinstance(sexp, PersistentMap):
        return PersistentMap.create({eval_sexp(key, env): eval_sexp(sexp[key], env) for key in sexp})
    else: # if the value is an atomic data type, cannot evaluate further
        return sexp

def eval_sexp(sexp, env, macro_call = False):
    """`eval_exp` evaluates a Symbolic Expression within a context.
    The context is the 'environment' a mapping of names to namespaces,
    and the namespace in which the execution is working at the moment.
    By default, execution starts in the `None` namespace, which corresponds to the standard library.
    """
    global loaded_ns
    in_loop   = False
    loop_sexp = None
    loop_env  = None
    loop_args = tuple()
    while True:
        # print(print_sexp(sexp))
        if not isinstance(sexp, PersistentList):
            return eval_primitive(sexp, env)

        # macroexpansion step
        sexp = macroexpand(sexp, env)

        # We need to check for primitive datatypes before and after macroexpansion
        if not isinstance(sexp, PersistentList):
            return eval_primitive(sexp, env)

        if len(sexp) == 0:
            return None
        ## Special Forms: ##
        # NOTE: is this needed?
        if isinstance(sexp[0], PersistentList):
            # sexp[0] = eval_sexp(sexp[0], env)
            sexp = PersistentList.create(eval_sexp(sexp[0], env), *sexp[1:])
        head = sexp[0]
        is_s = isinstance(head, Symbol)
        if is_s and "def" == head.name:
            if len(sexp) < 3:
                raise SimbaSyntaxError(f"\n\t`def` statement has invalid argument pattern in:\n\t{print_sexp(sexp)}")
            _name = sexp[1]
            _val = sexp[2]
            _res = eval_sexp(_val, env)
            env.ns.set(_name, (_var := Var(env.ns, _name, root = _res)).withMeta(_name.meta | _var.meta))
            return _var
        elif is_s and "quote" == head.name:
            if len(sexp) != 2: raise SimbaSyntaxError(f"\n\t`quote` expected 1 argument in:\n\t{print_sexp(sexp)}")
            return sexp[1]
        elif is_s and "if" == head.name:
            if len(sexp) < 3:
                raise SimbaSyntaxError(f"\n\tToo few arguments to if in:\n\t{print_sexp(sexp)}")
            if len(sexp) > 4:
                raise SimbaSyntaxError(f"\n\tToo many arguments to if in:\n\t{print_sexp(sexp)}")
            cond, then = sexp[1:3]
            evaled_cond = eval_sexp(cond, env)
            if evaled_cond is not None and evaled_cond is not False:
                sexp = then 
                continue # TCO
            else:
                if (len(sexp) == 4):
                    _else = sexp[3]
                    sexp = _else 
                    continue # TCO
                else: return None
        elif is_s and "fn" == head.name:
            offset = 0
            fn_name = None
            fn_optmap = None
            # optional name
            if isinstance(sexp[1], Symbol):
                offset = 1
                fn_name = sexp[1]
            # optional option map
            if len(sexp) >= 3 + offset and isinstance(sexp[2+offset], PersistentMap):
                fn_optmap = eval_sexp(sexp[2+offset], env)
            if isinstance(sexp[1+offset], PersistentVector):
                # anonymous function (single method declaration)
                argVector, body = sexp[1+offset], sexp[2+offset:]
                # what the closure should do is:
                # - gather all the free variables
                # - point to the local bindings in `bindings`
                bindings = env # this is temporary:
                # for now, the entire enclosing scope in referenced. This may impair garbage collection too much.
                # in the future, the bindings will be only the ones references in the closure
                return Function(argVector, body, bindings, optname = fn_name, optmap = fn_optmap)
            elif isinstance(sexp[1+offset], PersistentList):
                # anonymous multimethod (with multiple method declarations)
                fn = Function(sexp[1+offset][0], sexp[1+offset][1:], env, optname = fn_name, optmap = fn_optmap)
                for exp in sexp[2+offset:]:
                    # NOTE: here we do not attempt to parse optmap
                    # argVector, body = exp[0], exp[1:]
                    fn = fn.register(Function(exp[0], exp[1:], env))
                return fn
            raise SimbaSyntaxError(f"Wrong argument pattern for `fn` in {print_sexp(sexp)}")
        elif is_s and "do" == head.name:
            if len(sexp) == 1: return None
            for e in sexp[1:-1]:
                eval_sexp(e, env)
            sexp = sexp[-1]
            continue # TCO
        elif is_s and "let" == head.name:
            # creates a new environment and binds the values to it successively (in order)
            # evaluates the body in an implicit do
            if len(sexp) == 2: return None
            vec = sexp[1]
            env = Environment(outer = env)
            for i in range(0, len(vec), 2):
                env.set(vec[i], eval_sexp(vec[i+1], env))
            for exp in sexp[2:-1]:
                eval_sexp(exp, env)
            sexp = sexp[-1]
            continue # TCO
        elif is_s and "loop" == head.name:
            # loop is like let in that it provides immutable bindings
            # however it alters the state to know that we are in a loop
            # to understand what a tail position is, refer to:
            # http://www.r6rs.org/final/html/r6rs/r6rs-Z-H-14.html#node_sec_11.20
            if len(sexp) == 2: return None
            vec = sexp[1]
            env = Environment(outer = env)
            in_loop   = True
            loop_sexp = PersistentList.create(Symbol('do'), *sexp[2:])
            loop_env  = env
            loop_args = []
            for i in range(0, len(vec), 2):
                env.set(vec[i], eval_sexp(vec[i+1], env))
                loop_args.append(vec[i])
            for exp in sexp[2:-1]:
                eval_sexp(exp, env)
            sexp = sexp[-1]
            continue # TCO
        elif is_s and "recur" == head.name:
            if not in_loop: raise IllegalStateException(f"\nCannot use recur outside of a tail position in: \n {print_sexp(sexp)}.")
            # evaluate the arguments in the old env
            evaled_args = [eval_sexp(e, env) for e in sexp[1:]]
            # for i in range(len(loop_args)):
            #     env.set(loop_args[i], evaled_args[i])
            sexp = loop_sexp
            env  = loop_env
            # bind the new values to the new env
            env.names = bind_fn_args(loop_args, evaled_args, recur = True)
            # return to the top of the loop expression
            continue
        elif is_s and "." == head.name:
            # assumes the member to be a symbol, otherwise will throw
            target = eval_sexp(sexp[1], env)
            if isinstance(sexp[2], PersistentList):
                member = sexp[2][0].name
                args = sexp[2][1:]
            else:
                member = sexp[2].name
                args = sexp[3:]
            args = [eval_sexp(arg, env) for arg in args]
            if member.startswith('-'):
                return getattr(target, member)
            # from the Clojure doc: (modified)
            # If the first operand is a symbol that resolves to a class name, 
            # the access is considered to be to a static member of the named class. 
            # Note that nested classes are named EnclosingClass$NestedClass, per the 
            # JVM spec. Otherwise it is presumed to be an instance member and the first 
            # argument is evaluated to produce the target object.

            # according to the above a module doesnt resolve to a class and thus 
            # we should try to call the module functions
            if hasattr(target, member):
                a = getattr(target, member)
                if not isinstance(target, type) and callable(a):
                    return a(*args)
                else:
                    return a
            raise SimbaException(f"{target} has no attribute {member}")
        elif is_s and "var" == head.name:
            symbol = sexp[1]
            return env.get(symbol, deref_var = False)
        elif is_s and "try" == head.name:
            if len(sexp) == 4:
                try:
                    return eval_sexp(sexp[1], env)
                except Exception as e:
                    env.set(Symbol("*error*"), e)
                    return eval_sexp(sexp[2][1], env)
                finally:
                    eval_sexp(sexp[3][1], env)
            elif len(sexp) == 3 and sexp[2][0] == Symbol('catch'):
                try:
                    return eval_sexp(sexp[1], env)
                except Exception as e:
                    env.set(Symbol("*error*"), e)
                    return eval_sexp(sexp[2][1], env)
            elif len(sexp) == 3 and sexp[2][0] == Symbol('finally'):
                try:
                    return eval_sexp(sexp[1], env)
                finally:
                    eval_sexp(sexp[2][1], env)
            elif len(sexp) == 2:
                return eval_sexp(sexp[1], env)
            elif len(sexp) == 1:
                return None
            else:
                raise SimbaSyntaxError(f"Misformed try/catch expression in {print_sexp(sexp)}.")
        # ns stuff #
        elif is_s and "ns" == head.name:
            ns_name = sexp[1].name
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
            break
        elif is_s and "require" == head.name:
            require([sexp[1].name], env.ns)
            break
        elif is_s and "include" == head.name:
            require([sexp[1].name], env.ns, include=True)
            break
        # macros #
        elif is_s and "quasiquote" == head.name:
            sexp = quasiquote(sexp[1])
            continue # TCO
        elif is_s and "macroexpand" == head.name:
            if len(sexp) != 2: return Exception("`macroexpand` expected 1 argument.")
            return macroexpand(sexp[1], env)
        else:
            ## Non-Special Forms ##
            ## evaluate the args ##
            if not macro_call:
                evaluated_args = [eval_sexp(e, env) for e in sexp]
            else:
                # evaluated_args = sexp
                # add &form and &env
                evaluated_args = [sexp[0], sexp, env, *sexp[1:]]
                macro_call = False
            matched = False
            if isinstance(fun := evaluated_args[0], OverloadedFn):
                for tup in fun.method_table:
                    if signature_match(tup[0], evaluated_args[1:]):
                        fun = evaluated_args[0] = tup[1]
                        matched = True
                        break
                if not matched: raise MultipleDispatchException(f"No matching signature {evaluated_args} for multimethod {sexp[0].name}")
            if isinstance(fun, MultiFn):
                # evaluate the dispatch function
                val = eval_sexp(PersistentList.create(fun.dispatch_fn, *evaluated_args[1:]), env)
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
                    names = bind_fn_args(fun.args, evaluated_args[1:]) # args are the names of the env
                )
                # mark that we are inside a loop
                in_loop   = True
                loop_sexp = PersistentList.create(Symbol('do'), *fun.ast)
                loop_env  = env
                loop_args = fun.args
                # if the body is empty return `nil`
                if len(fun.ast) == 0:
                    return None
                for e in fun.ast[:-1]: eval_sexp(e, env)
                sexp = fun.ast[-1]
                continue
            else:
                ## apply the head ##
                # If we reach this point it means that the object in the head is a python callable
                # we must first parse the named arguments
                return fun(*evaluated_args[1:])


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