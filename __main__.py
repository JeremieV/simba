import sys, traceback
import antlr4
import reader

def eval(ast, env):
    return ast

def print(exp):
    return exp

def rep(stream):
    while (True):
        print(
            eval(
                reader.read(
                    stream,
                    environment={}
                )))

def run(file):
    input  = antlr4.FileStream(file, encoding='utf-8')
    with open(file, 'r') as f:
        code       = f.read()
        unindented = reader.addIndentationTokens(code)
        ds         = reader.read(antlr4.InputStream(unindented), {})
        result     = eval(ds, {})
        print(result)

# when called with no arguments, the command is a terminal repl
if __name__ == "__main__" and len(sys.argv) == 1:
    eof = False
    while not eof:
        try:
            # line = input('>>> ')
            # print('>>> ')
            print(rep(antlr4.StdinStream(encoding='utf-8')))
        except EOFError:
            eof = True
        except KeyboardInterrupt:
            print('Exit with Ctrl-D')
            eof = True
        except Exception as e:
            print("".join(traceback.format_exception(*sys.exc_info())))
# when called with the name of a file, will interpret that file
elif __name__ == "__main__" and len(sys.argv) > 1:
    run(sys.argv[1])


    
# lexer = simbaLexer(StdinStream())
# stream = CommonTokenStream(lexer)
# parser = simbaParser(stream)
# tree = parser.hi()
# printer = simbaPrintListener()
# walker = ParseTreeWalker()
# walker.walk(printer, tree)

# input  = FileStream(filename, encoding='utf-8') if filename else StdinStream(encoding='utf-8')