import re
from simbaTypes import (Symbol, Vector, Map, SymbolicExpression, Keyword)
from simbaTypes import *

class Blank(Exception): pass

class SexpReader():
    """Implementation of a recursive descent parser for s-expressions.
    Reads tokens one by one."""
    def __init__(self, text, position=0):
        self.tokens = tokenize(text)
        self.position = position

    def next(self):
        "Advance token position by one."
        self.position += 1
        return self.tokens[self.position-1]

    def peek(self):
        if len(self.tokens) > self.position:
            return self.tokens[self.position]
        else:
            return None

    def read_form(self):
        if self.position > len(self.tokens)-1: raise Exception("Token out of bounds exception")
        return read_form(self)

    def read_forms(self):
        ast = []
        while self.position < len(self.tokens):
            ast.append(read_form(self))

def _unescape(s):
    return s.replace('\\\\', '\u029e').replace('\\"', '"').replace('\\n', '\n').replace('\u029e', '\\')

def tokenize(str: str) -> list[str]:
        tre = re.compile(r"""[\s]*(~@|[\[\]{}()'`~^@]|"(?:[\\].|[^\\"])*"?|;.*|[^\s\[\]{}()'"`@,;]+)""");
        return [t for t in re.findall(tre, str) if t[0] != ';']

def read_atom(reader):
    int_re = re.compile(r"-?[0-9]+$")
    float_re = re.compile(r"-?[0-9][0-9.]*$")
    string_re = re.compile(r'"(?:[\\].|[^\\"])*"')
    token = reader.next()
    if re.match(int_re, token):     return int(token)
    elif re.match(float_re, token): return float(token)
    elif re.match(string_re, token):return _unescape(token[1:-1])
    elif token[0] == '"':           raise Exception("expected '\"', got EOF")
    elif token[0] == ':':           return Keyword(token[1:])
    elif token == "nil":            return None
    elif token == "true":           return True
    elif token == "false":          return False
    else:                           return Symbol(token) # here returns symbol

def read_sequence(reader, typ=list, start='(', end=')'):
    # ast = typ()
    token = reader.next()
    if token != start: raise Exception("expected '" + start + "'")

    arguments = []
    token = reader.peek()
    while token != end:
        if not token: raise Exception("expected '" + end + "', got EOF")
        arguments.append(read_form(reader))
        token = reader.peek()
    reader.next()
    # print(arguments)
    return typ(*arguments) if typ == SymbolicExpression else arguments

def readMap(reader):
    lst = read_sequence(reader, list, '{', '}')
    return dict(*lst)

def readSymbolicExpression(reader):
    return read_sequence(reader, SymbolicExpression, '(', ')')

def readVector(reader):
    return read_sequence(reader, Vector, '[', ']')

def read_form(reader):
    "Reads a single Simba form. Raises an exception for unmatched parens."
    token = reader.peek()
    # reader macros/transforms
    if token[0] == ';':
        reader.next()
        return None
    elif token == '\'':
        reader.next()
        return SymbolicExpression(Symbol('quote'), read_form(reader))
    elif token == '`':
        reader.next()
        return SymbolicExpression(Symbol('quasiquote'), read_form(reader))
    elif token == '~':
        reader.next()
        return SymbolicExpression(Symbol('unquote'), read_form(reader))
    elif token == '~@':
        reader.next()
        return SymbolicExpression(Symbol('splice-unquote'), read_form(reader))
    # elif token == '^':
    #     reader.next()
    #     meta = read_form(reader)
    #     return SymbolicExpression(Symbol('with-meta'), read_form(reader), meta)
    elif token == '@':
        reader.next()
        return SymbolicExpression(Symbol('deref'), read_form(reader))
    # elif token[0] == ':':
    #     _tok = token[1:]
    #     reader.next()
    #     f = read_form(reader)
    #     # named_arguments[-1][_tok] = f
    #     return AstIgnore()
    # list
    elif token == ')': raise Exception("unexpected ')'")
    elif token == '(': return readSymbolicExpression(reader)
    # vector
    elif token == ']': raise Exception("unexpected ']'")
    elif token == '[': return readVector(reader);
    # map
    elif token == '}': raise Exception("unexpected '}'")
    elif token == '{': return readMap(reader);
    # atom
    else:              return read_atom(reader)

# def read_str(str):
#     """read_str tokenizes the input string and returns a Simba data structures"""
#     tokens = tokenize(str)
#     # if len(tokens) == 0: raise Blank("Blank Line")
#     return read_form(SexpReader(tokens))

# =============================================================
#                          PRINTER
# =============================================================

def to_string(obj, indent=0, lb=True) -> str:
    def _escape(s): return s.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
    if lb:
        start = '\n'
    else:
        start = ''
    if type(obj) == SymbolicExpression:
        if obj.positional and obj.relational:
            return start + " "*indent + "(" + " ".join(to_string(e,indent=indent+2) for e in obj.positional) + " " + " ".join(to_string(Keyword(key), indent=indent+2) + " " + to_string(obj.relational[key], indent=indent+2) for key in obj.relational) + ")"
        elif obj.relational:
            return "(" + " ".join(to_string(Keyword(key), indent=indent, lb=lb) + " " + to_string(obj.relational[key], indent=indent+2) for key in obj.relational) + ")"
        else: return start + " "*indent + "(" + " ".join(to_string(e, indent=indent+2) for e in obj.positional) + ")"
    elif type(obj) == Vector:
        return "[" + " ".join(to_string(e) for e in obj) + "]"
    elif type(obj) == Map:
        ret = []
        for k in obj.keys():
            ret.extend((to_string(k), to_string(obj[k])))
        return "{" + " ".join(ret) + "}"
    elif type(obj) == Keyword:
        return start + " "*indent + ':' + str(obj)
    elif type(obj) == str:
        # if len(obj) > 0 and obj[0] == '\u029e':
        #     return ':' + obj[1:]
        return '"' + _escape(obj) + '"'
    elif obj is None:
        return "nil"
    elif obj is True:
        return "true"
    elif obj is False:
        return "false"
    else:
        # print(type(obj))
        return obj.__str__()