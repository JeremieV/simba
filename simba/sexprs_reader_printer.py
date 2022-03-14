import re
from simba.simba_types import (Symbol, Vector, Map, SymbolicExpression, Keyword, Namespace)
import pyrsistent as p
import pvectorc

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
    elif token[0] == '.':           return token[1:]
    elif token == "nil":            return None
    elif token == "true":           return True
    elif token == "false":          return False
    else:                           return Symbol(token) # here returns symbol

def read_sequence(reader, start='(', end=')'):
    token = reader.next()
    if token != start: raise Exception("expected '" + start + "'")

    arguments = []
    token = reader.peek()
    while token != end:
        if not token: raise Exception("expected '" + end + "', got EOF")
        if token[0] == '.':
            # in the midst of this if clause
            arguments.append(Symbol('get-attr'))
            arguments.append(read_form(reader))
        arguments.append(read_form(reader))
        token = reader.peek()
    reader.next()
    # print(arguments)
    return arguments

def readMap(reader):
    lst = read_sequence(reader, '{', '}')
    m = {}
    for name, value in zip(lst[0::2], lst[1::2]):
        if isinstance(value, Keyword):
            raise Exception("A map can only have keywords as keys.")
        if isinstance(name, Keyword):
            name = str(name)
        m[name] = value
    return p.pmap(m)

def readSymbolicExpression(reader):
    return SymbolicExpression(*read_sequence(reader, '(', ')'))

def readVector(reader):
    return p.pvector(read_sequence(reader, '[', ']'))

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
    if isinstance(obj, SymbolicExpression):
        if obj.positional and obj.relational:
            return start + " "*indent + "(" + " ".join(to_string(e,indent=indent+2) for e in obj.positional) + " " + " ".join(to_string(Keyword(key), indent=indent+2) + " " + to_string(obj.relational[key], indent=indent+2) for key in obj.relational) + ")"
        elif obj.relational:
            return "(" + " ".join(to_string(Keyword(key), indent=indent, lb=lb) + " " + to_string(obj.relational[key], indent=indent+2) for key in obj.relational) + ")"
        else: return start + " "*indent + "(" + " ".join(to_string(e, indent=indent+2) for e in obj.positional) + ")"
    elif isinstance(obj, Vector):
        return "[" + " ".join(to_string(e) for e in obj) + "]"
    elif isinstance(obj, Map):
        return "{" + " ".join(to_string(k, indent=indent, lb=lb) + " " + to_string(obj[k], indent=indent, lb=lb) + "\n" for k in obj) + "}"
    elif isinstance(obj, Keyword):
        return start + " "*indent + ':' + str(obj)
    elif isinstance(obj, str):
        # if len(obj) > 0 and obj[0] == '\u029e':
        #     return ':' + obj[1:]
        return '"' + _escape(obj) + '"'
    elif obj is None:
        return "nil"
    elif obj is True:
        return "true"
    elif obj is False:
        return "false"
    elif isinstance(obj, Namespace):
        return f"#namespace[{obj.name}]"
    else:
        # print(type(obj))
        return obj.__str__()