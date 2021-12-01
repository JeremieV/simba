import antlr4
from simbaTypes import *
from antlr4.tree.Tree import ParseTreeWalker
# from grammar.simbaLexer import simbaLexer
# from grammar.simbaParser import simbaParser
# from grammar.simbaListener import simbaListener
import itertools

def read(inputStream, environment):
    # print('=== Output ===')
    lexer  = simbaLexer(inputStream)
    stream = antlr4.CommonTokenStream(lexer)
    parser = simbaParser(stream)
    tree   = parser.start()
    # print(tree.toStringTree(recog=parser))

    # listener = antlr4.ParseTreeListener()
    # ParseTreeWalker.DEFAULT.walk(listener, tree)

    # printer = simbaPrintListener()
    # walker = ParseTreeWalker()
    # walker.walk(printer, tree)
    # return dataStructure

def addIndentationTokens(input):
    """ 
        Before lexing and parsing we must insert tokens that stand for
        the start and end of an indented block in the source file. 
        The indentation rules follow these from the official python 
        reference: <https://docs.python.org/3.3/reference/lexical_analysis.html#indentation>

        Importantly, this script only adds to the end of exiting lines.
        Hence it does not affect line and column numbers in error reporting. 

        Input and output are strings for now.
    """
    stack = [0]
    indent = ' > ' # ' 🐼 '
    dedent = ' < ' # ' 🐨 '
    new = []
    for line_number, line in enumerate(input.split('\n')):
        if line.isspace() or line == "":
            new.append('')
            continue
        leadingSpaces = sum(1 for _ in itertools.takewhile(str.isspace, line))
        if stack[-1] < leadingSpaces:
            stack.append(leadingSpaces)
            new[-1] = new[-1] + indent
        else:
            while stack[-1] > leadingSpaces:
                stack.pop() 
                if stack[-1] < leadingSpaces:
                    raise IndentationError(f'Line number {line_number} is not indented properly.')
                new[-1] = new[-1] + dedent
        new.append(line)
    # handle end of file
    for _ in stack[1:]:
        new[-1] = new[-1] + dedent
    output = '\n'.join(new)
    return output


# output = re.sub(
#     r'(?<=[^\(]\s)[a-zA-Z]+\.',
#     lambda match: '(' + match.group(),
#     code,
#     count=1
# )

# ================================================================
#                              PRINTER
# ================================================================

def to_string(obj, indent = 0):
    def _escape(s): return s.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
    if type(obj) == SymbolicExpression:
        return obj.head + ". " + " ".join(map(lambda e: to_string(e), obj.positional))
    elif type(obj) == Vector:                                    
        return "[" + " ".join(map(lambda e: to_string(e), obj)) + "]"
    elif type(obj) == Map:
        ret = []
        for k in obj.keys():
            ret.extend((to_string(k), to_string(obj[k])))
        return "{" + " ".join(ret) + "}"
    elif type(obj) == str:
        return '"' + _escape(obj) + '"'
    elif type(obj) == None:
        return "nil"
    elif type(obj) == True:
        return "true"
    elif type(obj) == False:
        return "false"
    # elif type(obj) == Atom:
    #     return "(atom " + to_string(obj.val,_r) + ")"
    else:
        return obj.__str__()