# Generated from simba.g4 by ANTLR 4.9.2
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
    from typing import TextIO
else:
    from typing.io import TextIO



def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\2\22")
        buf.write("g\b\1\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7")
        buf.write("\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\4\r\t\r\4\16")
        buf.write("\t\16\4\17\t\17\4\20\t\20\4\21\t\21\4\22\t\22\3\2\3\2")
        buf.write("\3\3\3\3\3\3\5\3+\n\3\3\4\3\4\3\4\7\4\60\n\4\f\4\16\4")
        buf.write("\63\13\4\3\4\3\4\3\4\3\4\7\49\n\4\f\4\16\4<\13\4\3\4\5")
        buf.write("\4?\n\4\3\5\3\5\3\5\3\6\6\6E\n\6\r\6\16\6F\3\7\3\7\3\7")
        buf.write("\3\b\3\b\3\t\3\t\3\n\3\n\3\n\3\n\3\13\3\13\3\13\3\f\6")
        buf.write("\fX\n\f\r\f\16\fY\3\r\3\r\3\16\3\16\3\17\3\17\3\20\3\20")
        buf.write("\3\21\3\21\3\22\3\22\2\2\23\3\3\5\4\7\5\t\2\13\6\r\7\17")
        buf.write("\b\21\t\23\n\25\13\27\f\31\r\33\16\35\17\37\20!\21#\22")
        buf.write("\3\2\7\6\2\f\f\16\17))^^\6\2\f\f\16\17$$^^\4\2C\\c|\5")
        buf.write("\2\f\f\17\17\"\"\3\2\62;\2n\2\3\3\2\2\2\2\5\3\2\2\2\2")
        buf.write("\7\3\2\2\2\2\13\3\2\2\2\2\r\3\2\2\2\2\17\3\2\2\2\2\21")
        buf.write("\3\2\2\2\2\23\3\2\2\2\2\25\3\2\2\2\2\27\3\2\2\2\2\31\3")
        buf.write("\2\2\2\2\33\3\2\2\2\2\35\3\2\2\2\2\37\3\2\2\2\2!\3\2\2")
        buf.write("\2\2#\3\2\2\2\3%\3\2\2\2\5*\3\2\2\2\7>\3\2\2\2\t@\3\2")
        buf.write("\2\2\13D\3\2\2\2\rH\3\2\2\2\17K\3\2\2\2\21M\3\2\2\2\23")
        buf.write("O\3\2\2\2\25S\3\2\2\2\27W\3\2\2\2\31[\3\2\2\2\33]\3\2")
        buf.write("\2\2\35_\3\2\2\2\37a\3\2\2\2!c\3\2\2\2#e\3\2\2\2%&\7=")
        buf.write("\2\2&\4\3\2\2\2\'+\5\13\6\2(+\5\27\f\2)+\5\7\4\2*\'\3")
        buf.write("\2\2\2*(\3\2\2\2*)\3\2\2\2+\6\3\2\2\2,\61\7)\2\2-\60\5")
        buf.write("\t\5\2.\60\n\2\2\2/-\3\2\2\2/.\3\2\2\2\60\63\3\2\2\2\61")
        buf.write("/\3\2\2\2\61\62\3\2\2\2\62\64\3\2\2\2\63\61\3\2\2\2\64")
        buf.write("?\7)\2\2\65:\7$\2\2\669\5\t\5\2\679\n\3\2\28\66\3\2\2")
        buf.write("\28\67\3\2\2\29<\3\2\2\2:8\3\2\2\2:;\3\2\2\2;=\3\2\2\2")
        buf.write("<:\3\2\2\2=?\7$\2\2>,\3\2\2\2>\65\3\2\2\2?\b\3\2\2\2@")
        buf.write("A\7^\2\2AB\13\2\2\2B\n\3\2\2\2CE\t\4\2\2DC\3\2\2\2EF\3")
        buf.write("\2\2\2FD\3\2\2\2FG\3\2\2\2G\f\3\2\2\2HI\5\13\6\2IJ\7\60")
        buf.write("\2\2J\16\3\2\2\2KL\7@\2\2L\20\3\2\2\2MN\7>\2\2N\22\3\2")
        buf.write("\2\2OP\t\5\2\2PQ\3\2\2\2QR\b\n\2\2R\24\3\2\2\2ST\7\13")
        buf.write("\2\2TU\b\13\3\2U\26\3\2\2\2VX\t\6\2\2WV\3\2\2\2XY\3\2")
        buf.write("\2\2YW\3\2\2\2YZ\3\2\2\2Z\30\3\2\2\2[\\\7*\2\2\\\32\3")
        buf.write("\2\2\2]^\7+\2\2^\34\3\2\2\2_`\7]\2\2`\36\3\2\2\2ab\7_")
        buf.write("\2\2b \3\2\2\2cd\7}\2\2d\"\3\2\2\2ef\7\177\2\2f$\3\2\2")
        buf.write("\2\13\2*/\618:>FY\4\b\2\2\3\13\2")
        return buf.getvalue()


class simbaLexer(Lexer):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    T__0 = 1
    LITERAL = 2
    STRING = 3
    NAME = 4
    OPERATOR = 5
    INDENT = 6
    DEDENT = 7
    WS = 8
    TAB = 9
    NUMBER = 10
    LPAREN = 11
    RPAREN = 12
    LSSQUARE = 13
    RSSQUARE = 14
    LCURLY = 15
    RCURLY = 16

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
            "';'", "'>'", "'<'", "'\t'", "'('", "')'", "'['", "']'", "'{'", 
            "'}'" ]

    symbolicNames = [ "<INVALID>",
            "LITERAL", "STRING", "NAME", "OPERATOR", "INDENT", "DEDENT", 
            "WS", "TAB", "NUMBER", "LPAREN", "RPAREN", "LSSQUARE", "RSSQUARE", 
            "LCURLY", "RCURLY" ]

    ruleNames = [ "T__0", "LITERAL", "STRING", "STRING_ESCAPE_SEQ", "NAME", 
                  "OPERATOR", "INDENT", "DEDENT", "WS", "TAB", "NUMBER", 
                  "LPAREN", "RPAREN", "LSSQUARE", "RSSQUARE", "LCURLY", 
                  "RCURLY" ]

    grammarFileName = "simba.g4"

    def __init__(self, input=None, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.9.2")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None


    def action(self, localctx:RuleContext, ruleIndex:int, actionIndex:int):
        if self._actions is None:
            actions = dict()
            actions[9] = self.TAB_action 
            self._actions = actions
        action = self._actions.get(ruleIndex, None)
        if action is not None:
            action(localctx, actionIndex)
        else:
            raise Exception("No registered action for:" + str(ruleIndex))


    def TAB_action(self, localctx:RuleContext , actionIndex:int):
        if actionIndex == 0:
             raise TabError('You should not use tabs in Simba source code.')  
     


