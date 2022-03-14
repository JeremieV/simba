import os
from simba.simba_exceptions import MultipleNamespacesError, NoNamespaceError
import simba.sexprs_reader_printer as sexprs_reader_printer

def reverse(lst):
    return [ele for ele in reversed(lst)]

def read_files(reader, files):
    """Opens, reads, and closes the files in order.
    If the filename points to a directory, then read all the files in that directory.
    (and all the files in all the subdirectories).
    Returns a Simba Symbolic Expression."""
    ast_list = []
    for file in files:
        if os.path.isdir(file):
            for name in os.listdir(file):
                if file[-1] == '/':
                    ast_list += read_files(reader, [file + name])
                else:
                    ast_list += read_files(reader, ['/'.join([file, name])])
        else:
            with open(file, 'r') as f:
                if file[-3:] == ".sb":    
                    program = f.read()
                    readerObj = reader.SexpReader(program)
                    while readerObj.position < len(readerObj.tokens):
                        e = readerObj.read_form()
                        ast_list.append(e)
    return ast_list

def read_files_form_by_form(reader, procedure, files):
    """Same as read_files except that it reads the forms one by one and it can take a procedure to execute on each form.
    This function allows one to perform an operation on the data in one pass, unlike read_files.
    Furthermore, it is takes roughly 'constant' space where read_files takes linear space."""
    for file in files:
        with open(file, 'r') as f:
            program = f.read()
            readerObj = reader.SexpReader(program)
            while readerObj.position < len(readerObj.tokens):
                e = readerObj.read_form()
                procedure(e)

def read_string_eager(string, reader = sexprs_reader_printer):
    ast_list = []
    readerObj = reader.SexpReader(string)
    while readerObj.position < len(readerObj.tokens):
        e = readerObj.read_form()
        ast_list.append(e)
    return ast_list

def read_string_form_by_form(reader, procedure, string):
    """Similar to read_files_form_by_form, useful for the REPL."""
    readerObj = reader.SexpReader(string)
    while readerObj.position < len(readerObj.tokens):
        e = readerObj.read_form()
        procedure(e)

def find_forms(startswith, ast_list):
    """Finds the forms that begin with the elements in the startwith argument."""
    results = []
    for f in ast_list:
        is_match = True
        for i, val in enumerate(f[:len(startswith)]):
            if val.name != startswith[i]:
                is_match = False
        if is_match: results.append(f)
    return results

def find_test_ns(ast_list):
    """Finds all the test namespaces in the ast, which are all the namespaces that have a name ending in '-test'."""
    results = []
    for f in ast_list:
        if f[0].name == "ns" and f[1].name[-5:] == "-test":
            results.append(f)
    return results

def find_ns(name, ast_list):
    """Finds the namespace of a given name in the AST."""
    res = find_forms(["ns", name], ast_list)
    if len(res) > 1:
        raise Exception(f"There is more than one `{name}` namespace.")
    if len(res) == 0:
        raise Exception(f"No `{name}` namespace was found.")
    return res[0]

def return_ns(name, ast_list):
    from simba.simba_types import Symbol, SymbolicExpression
    res = []
    is_found = False
    adding = False
    for exp in ast_list:
        cond = isinstance(exp, SymbolicExpression)
        if cond and exp[0] == Symbol("ns") and exp[1] == Symbol(name):
            if is_found: raise MultipleNamespacesError(f"Multiple namespaces of the name {name} were found.")
            is_found = True
            adding = True
        elif cond and exp[0] == Symbol("ns"):
            adding = False
        if adding:
            res.append(exp)
    if not is_found: raise NoNamespaceError(f"No namespace of the name {name} was found.")
    return res

def return_test_ns(ast_list):
    from simba.simba_types import Symbol, SymbolicExpression
    res = []
    is_test = False
    is_found = False
    for exp in ast_list:
        cond = isinstance(exp, SymbolicExpression)
        if cond and exp[0] == Symbol("ns") and isinstance(exp[1], Symbol) and exp[1].name[-5:] == "-test":
            res.append([])
            is_test = True
            is_found = True
        elif cond and exp[0] == Symbol("ns"):
            is_test = False
        if is_test:
            res[-1].append(exp)
    if not is_found: raise NoNamespaceError(f"No test namespace was found.")
    return res

def get_base_namespace(reader):
    return read_files(reader, ['libraries/base.sb'])

#== Exec except that it returns the value ==#
# Taken from https://stackoverflow.com/questions/33409207/how-to-return-value-from-exec-in-function

import ast
import copy
def convertExpr2Expression(Expr):
        Expr.lineno = 0
        Expr.col_offset = 0
        result = ast.Expression(Expr.value, lineno=0, col_offset = 0)

        return result
def exec_with_return(code):
    code_ast = ast.parse(code)

    init_ast = copy.deepcopy(code_ast)
    init_ast.body = code_ast.body[:-1]

    last_ast = copy.deepcopy(code_ast)
    last_ast.body = code_ast.body[-1:]

    exec(compile(init_ast, "<ast>", "exec"), globals())
    if type(last_ast.body[0]) == ast.Expr:
        return eval(compile(convertExpr2Expression(last_ast.body[0]), "<ast>", "eval"),globals())
    else:
        exec(compile(last_ast, "<ast>", "exec"),globals())