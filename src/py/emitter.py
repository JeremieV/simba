import ast
from simbaTypes import *
import simba
import helpers
import reader

s = SymbolicExpression(Symbol('if'), True, 1, 0)

src = """\
(if true 1 0)
"""

readerObj = helpers.read_string_eager()



print(ast.dump(ast.parse('from y import x,y,z'), indent=4))

# https://python-ast-explorer.com/
# https://github.com/octoml/synr