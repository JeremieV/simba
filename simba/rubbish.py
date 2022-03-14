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

# def eval_sexp(sexp, env):
#     """
#     eval_exp evaluates a Symbolic Expression within a context.
#     The context is the 'environment' a mapping of names to namespaces,
#     and the namespace in which the execution is working at the moment.
#     By default, execution starts in the `None` namespace, which corresponds to the standard library.
#     """
#     if (isinstance(sexp, Symbol)): # if symbol evaluate to its binding
#         try: return env.get(sexp)
#         except KeyError: raise UnresolvedSymbolError(sexp)
#     # elif map
#     # elif vector
#     elif (isinstance(sexp, SymbolicExpression)): # apply the symbolic expression
#         if len(sexp.positional) == 0:
#             return None
#         ## Special Forms: ##
#         head = sexp.positional[0]
#         if "def" == head.name:
#             ## def adds a binding (from unevaluated first arg to evaled second arg) in the environment ##
#             a1, a2 = sexp.positional[1], sexp.positional[2]
#             res = eval_sexp(a2, env)
#             return env.set(a1, res)
#         elif "quote" == head.name:
#             if len(sexp.positional) != 2: raise Exception("quote expected 1 argument")
#             return sexp.positional[1]
#         elif "if" == head.name:
#             ## If may need some more work: what is truthy? what if fewer then 3 args? ##
#             if (len(sexp.positional) < 3):
#                 raise SyntaxError("Too few arguments to if")
#             if (len(sexp.positional) > 4):
#                 raise SyntaxError("Too many arguments to if")
#             cond, then = sexp.positional[1:3]
#             if cond:
#                 return eval_sexp(then, env)
#             else:
#                 if (len(sexp.positional) == 4):
#                     _else = sexp.positional[3]
#                     return eval_sexp(_else, env)
#                 else: return None
#         elif "fn" == head.name:
#             ## Anonymous function ##
#             ## returns a new closure ##
#             argVector, body = sexp.positional[1], sexp.positional[2:]
#             # what the closure should do is:
#             # - gather all the free variables
#             # - point to the local bindings in `bindings`
#             bindings = env # this is temporary: 
#             # for now, the entire enclosing scope in copied
#             # in the future, the bindings will be only the ones references in the closure
#             return Function(argVector, body, bindings)
#         elif "do" == head.name:
#             last = None
#             for exp in sexp.positional[1:]:
#                 last = eval_sexp(exp, env)
#             return last
#         elif "comment" == head.name:
#             return None
#         elif "let" == head.name:
#             ## creates a new environment and binds the values to it successively (in order) ##
#             vec, body = sexp.positional[1], sexp.positional[2:]
#             let_env = SimbaEnvironment(outer = env)
#             for i in range(0, len(vec), 2):
#                 let_env.set(vec[i], eval_sexp(vec[i+1], let_env))
#             ## evaluate the body in an implicit do ##
#             last = None
#             for exp in body:
#                 last = eval_sexp(exp, let_env)
#             return last
#         # elif type(head) == function:
#         #     ## Call a native function ##
#         #     return head(*sexp.positional[1:], **sexp.relational)
#         elif "ns" == head.name:
#             # ## If the namespace is 
#             # ## add a ns to the environment, and "jump" into it for evaluation ##
#             # if len(sexp.positional) != 2:
#             #     raise SyntaxError("The `namespace` form should have one argument.")
#             # # 1. Initialize the namespace and add it to the namespaces
#             # new_ns = sexp.positional[1]
#             # namespaces[new_ns] = SimbaEnvironment()
#             # # 2. Jump into the namespace to start evaluation

#             # print(env)
#             last = None
#             for exp in sexp.positional[2:]:
#                 last = eval_sexp(exp, env)
#             return last
#         else:
#             ## Non-Special Forms ##
#             ## evaluate the args ##
#             evaledPArgs = [eval_sexp(e, env) for e in sexp.positional]
#             evaledRArgs = {eval_sexp(key, env): eval_sexp(value, env) for key, value in sexp.relational}
#             ## apply the head ##
#             return evaledPArgs[0](*evaledPArgs[1:], **evaledRArgs)
#     else: # if the value is an atomic data type, cannot evaluate further
#         return sexp

# def eval_str(string):
#     exec_environment = SimbaEnvironment(names = repl_env)
#     readerObj = _reader.SexpReader(string)
#     result = None
#     while readerObj.position < len(readerObj.tokens):
#         e = readerObj.read_form()
#         result = eval_sexp(e, exec_environment)
#     return result

# elif "for" == head.name:
#     res = None
#     for 
# elif "while" == head.name:
#     cond = sexp.positional[1]
#     body = cond.positional[2:]
#     while ns_eval_sexp(cond, env, loaded_namespaces):
#         ns_eval_sexp(body, env, ns_eval_sexp)
# elif "loop" == head.name:
#     # ensure recur is at tail position
#     bindings = sexp[1] # hopefully the first argument is a vector
#     # ensure that the recur happens at the tails of the expr
#     contents = sexp[2:]
#     # val = 
#     while true:
#         # when you encounter recur, call next
#         # at the end, call break

# print(isinstance(pyrsistent.pvector([1, 2, 3]), collections.abc.Sequence))

a = {b'op': b'eval', b'code': b'*ns*', b'id': b'1'}
print(type(b'op'))

print(isinstance(b'op', bytes))
# print(a.items())

# https://python-ast-explorer.com/
# https://github.com/octoml/synr