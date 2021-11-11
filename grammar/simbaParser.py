# Generated from simba.g4 by ANTLR 4.9.2
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO


def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3\22")
        buf.write("T\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\3\2\7\2\16\n")
        buf.write("\2\f\2\16\2\21\13\2\3\2\3\2\3\3\3\3\3\3\3\3\3\3\7\3\32")
        buf.write("\n\3\f\3\16\3\35\13\3\3\3\3\3\7\3!\n\3\f\3\16\3$\13\3")
        buf.write("\3\3\5\3\'\n\3\3\3\3\3\3\3\3\3\5\3-\n\3\3\4\3\4\7\4\61")
        buf.write("\n\4\f\4\16\4\64\13\4\3\4\3\4\3\5\3\5\3\5\3\5\7\5<\n\5")
        buf.write("\f\5\16\5?\13\5\3\5\3\5\3\6\3\6\7\6E\n\6\f\6\16\6H\13")
        buf.write("\6\3\6\3\6\7\6L\n\6\f\6\16\6O\13\6\3\6\5\6R\n\6\3\6\4")
        buf.write("FM\2\7\2\4\6\b\n\2\2\2[\2\17\3\2\2\2\4,\3\2\2\2\6.\3\2")
        buf.write("\2\2\b\67\3\2\2\2\nB\3\2\2\2\f\16\5\4\3\2\r\f\3\2\2\2")
        buf.write("\16\21\3\2\2\2\17\r\3\2\2\2\17\20\3\2\2\2\20\22\3\2\2")
        buf.write("\2\21\17\3\2\2\2\22\23\7\2\2\3\23\3\3\2\2\2\24-\7\4\2")
        buf.write("\2\25-\5\6\4\2\26-\5\b\5\2\27\33\7\7\2\2\30\32\5\4\3\2")
        buf.write("\31\30\3\2\2\2\32\35\3\2\2\2\33\31\3\2\2\2\33\34\3\2\2")
        buf.write("\2\34&\3\2\2\2\35\33\3\2\2\2\36\"\7\b\2\2\37!\5\4\3\2")
        buf.write(" \37\3\2\2\2!$\3\2\2\2\" \3\2\2\2\"#\3\2\2\2#%\3\2\2\2")
        buf.write("$\"\3\2\2\2%\'\7\t\2\2&\36\3\2\2\2&\'\3\2\2\2\'-\3\2\2")
        buf.write("\2()\7\r\2\2)*\5\4\3\2*+\7\16\2\2+-\3\2\2\2,\24\3\2\2")
        buf.write("\2,\25\3\2\2\2,\26\3\2\2\2,\27\3\2\2\2,(\3\2\2\2-\5\3")
        buf.write("\2\2\2.\62\7\17\2\2/\61\5\4\3\2\60/\3\2\2\2\61\64\3\2")
        buf.write("\2\2\62\60\3\2\2\2\62\63\3\2\2\2\63\65\3\2\2\2\64\62\3")
        buf.write("\2\2\2\65\66\7\20\2\2\66\7\3\2\2\2\67=\7\21\2\289\5\4")
        buf.write("\3\29:\5\4\3\2:<\3\2\2\2;8\3\2\2\2<?\3\2\2\2=;\3\2\2\2")
        buf.write("=>\3\2\2\2>@\3\2\2\2?=\3\2\2\2@A\7\22\2\2A\t\3\2\2\2B")
        buf.write("F\7\3\2\2CE\13\2\2\2DC\3\2\2\2EH\3\2\2\2FG\3\2\2\2FD\3")
        buf.write("\2\2\2GQ\3\2\2\2HF\3\2\2\2IM\7\b\2\2JL\13\2\2\2KJ\3\2")
        buf.write("\2\2LO\3\2\2\2MN\3\2\2\2MK\3\2\2\2NP\3\2\2\2OM\3\2\2\2")
        buf.write("PR\7\t\2\2QI\3\2\2\2QR\3\2\2\2R\13\3\2\2\2\f\17\33\"&")
        buf.write(",\62=FMQ")
        return buf.getvalue()


class simbaParser ( Parser ):

    grammarFileName = "simba.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "';'", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "'>'", "'<'", "<INVALID>", "'\t'", "<INVALID>", 
                     "'('", "')'", "'['", "']'", "'{'", "'}'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "LITERAL", "STRING", "NAME", 
                      "OPERATOR", "INDENT", "DEDENT", "WS", "TAB", "NUMBER", 
                      "LPAREN", "RPAREN", "LSSQUARE", "RSSQUARE", "LCURLY", 
                      "RCURLY" ]

    RULE_start = 0
    RULE_form = 1
    RULE_sequence = 2
    RULE_association = 3
    RULE_comment = 4

    ruleNames =  [ "start", "form", "sequence", "association", "comment" ]

    EOF = Token.EOF
    T__0=1
    LITERAL=2
    STRING=3
    NAME=4
    OPERATOR=5
    INDENT=6
    DEDENT=7
    WS=8
    TAB=9
    NUMBER=10
    LPAREN=11
    RPAREN=12
    LSSQUARE=13
    RSSQUARE=14
    LCURLY=15
    RCURLY=16

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.9.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class StartContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EOF(self):
            return self.getToken(simbaParser.EOF, 0)

        def form(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(simbaParser.FormContext)
            else:
                return self.getTypedRuleContext(simbaParser.FormContext,i)


        def getRuleIndex(self):
            return simbaParser.RULE_start

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStart" ):
                listener.enterStart(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStart" ):
                listener.exitStart(self)




    def start(self):

        localctx = simbaParser.StartContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_start)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 13
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << simbaParser.LITERAL) | (1 << simbaParser.OPERATOR) | (1 << simbaParser.LPAREN) | (1 << simbaParser.LSSQUARE) | (1 << simbaParser.LCURLY))) != 0):
                self.state = 10
                self.form()
                self.state = 15
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 16
            self.match(simbaParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FormContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LITERAL(self):
            return self.getToken(simbaParser.LITERAL, 0)

        def sequence(self):
            return self.getTypedRuleContext(simbaParser.SequenceContext,0)


        def association(self):
            return self.getTypedRuleContext(simbaParser.AssociationContext,0)


        def OPERATOR(self):
            return self.getToken(simbaParser.OPERATOR, 0)

        def form(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(simbaParser.FormContext)
            else:
                return self.getTypedRuleContext(simbaParser.FormContext,i)


        def INDENT(self):
            return self.getToken(simbaParser.INDENT, 0)

        def DEDENT(self):
            return self.getToken(simbaParser.DEDENT, 0)

        def LPAREN(self):
            return self.getToken(simbaParser.LPAREN, 0)

        def RPAREN(self):
            return self.getToken(simbaParser.RPAREN, 0)

        def getRuleIndex(self):
            return simbaParser.RULE_form

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterForm" ):
                listener.enterForm(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitForm" ):
                listener.exitForm(self)




    def form(self):

        localctx = simbaParser.FormContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_form)
        self._la = 0 # Token type
        try:
            self.state = 42
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [simbaParser.LITERAL]:
                self.enterOuterAlt(localctx, 1)
                self.state = 18
                self.match(simbaParser.LITERAL)
                pass
            elif token in [simbaParser.LSSQUARE]:
                self.enterOuterAlt(localctx, 2)
                self.state = 19
                self.sequence()
                pass
            elif token in [simbaParser.LCURLY]:
                self.enterOuterAlt(localctx, 3)
                self.state = 20
                self.association()
                pass
            elif token in [simbaParser.OPERATOR]:
                self.enterOuterAlt(localctx, 4)
                self.state = 21
                self.match(simbaParser.OPERATOR)
                self.state = 25
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,1,self._ctx)
                while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                    if _alt==1:
                        self.state = 22
                        self.form() 
                    self.state = 27
                    self._errHandler.sync(self)
                    _alt = self._interp.adaptivePredict(self._input,1,self._ctx)

                self.state = 36
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,3,self._ctx)
                if la_ == 1:
                    self.state = 28
                    self.match(simbaParser.INDENT)
                    self.state = 32
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    while (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << simbaParser.LITERAL) | (1 << simbaParser.OPERATOR) | (1 << simbaParser.LPAREN) | (1 << simbaParser.LSSQUARE) | (1 << simbaParser.LCURLY))) != 0):
                        self.state = 29
                        self.form()
                        self.state = 34
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)

                    self.state = 35
                    self.match(simbaParser.DEDENT)


                pass
            elif token in [simbaParser.LPAREN]:
                self.enterOuterAlt(localctx, 5)
                self.state = 38
                self.match(simbaParser.LPAREN)
                self.state = 39
                self.form()
                self.state = 40
                self.match(simbaParser.RPAREN)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class SequenceContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LSSQUARE(self):
            return self.getToken(simbaParser.LSSQUARE, 0)

        def RSSQUARE(self):
            return self.getToken(simbaParser.RSSQUARE, 0)

        def form(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(simbaParser.FormContext)
            else:
                return self.getTypedRuleContext(simbaParser.FormContext,i)


        def getRuleIndex(self):
            return simbaParser.RULE_sequence

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSequence" ):
                listener.enterSequence(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSequence" ):
                listener.exitSequence(self)




    def sequence(self):

        localctx = simbaParser.SequenceContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_sequence)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 44
            self.match(simbaParser.LSSQUARE)
            self.state = 48
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << simbaParser.LITERAL) | (1 << simbaParser.OPERATOR) | (1 << simbaParser.LPAREN) | (1 << simbaParser.LSSQUARE) | (1 << simbaParser.LCURLY))) != 0):
                self.state = 45
                self.form()
                self.state = 50
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 51
            self.match(simbaParser.RSSQUARE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AssociationContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LCURLY(self):
            return self.getToken(simbaParser.LCURLY, 0)

        def RCURLY(self):
            return self.getToken(simbaParser.RCURLY, 0)

        def form(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(simbaParser.FormContext)
            else:
                return self.getTypedRuleContext(simbaParser.FormContext,i)


        def getRuleIndex(self):
            return simbaParser.RULE_association

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAssociation" ):
                listener.enterAssociation(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAssociation" ):
                listener.exitAssociation(self)




    def association(self):

        localctx = simbaParser.AssociationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_association)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 53
            self.match(simbaParser.LCURLY)
            self.state = 59
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << simbaParser.LITERAL) | (1 << simbaParser.OPERATOR) | (1 << simbaParser.LPAREN) | (1 << simbaParser.LSSQUARE) | (1 << simbaParser.LCURLY))) != 0):
                self.state = 54
                self.form()
                self.state = 55
                self.form()
                self.state = 61
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 62
            self.match(simbaParser.RCURLY)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class CommentContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def INDENT(self):
            return self.getToken(simbaParser.INDENT, 0)

        def DEDENT(self):
            return self.getToken(simbaParser.DEDENT, 0)

        def getRuleIndex(self):
            return simbaParser.RULE_comment

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterComment" ):
                listener.enterComment(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitComment" ):
                listener.exitComment(self)




    def comment(self):

        localctx = simbaParser.CommentContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_comment)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 64
            self.match(simbaParser.T__0)
            self.state = 68
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,7,self._ctx)
            while _alt!=1 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1+1:
                    self.state = 65
                    self.matchWildcard() 
                self.state = 70
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,7,self._ctx)

            self.state = 79
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==simbaParser.INDENT:
                self.state = 71
                self.match(simbaParser.INDENT)
                self.state = 75
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,8,self._ctx)
                while _alt!=1 and _alt!=ATN.INVALID_ALT_NUMBER:
                    if _alt==1+1:
                        self.state = 72
                        self.matchWildcard() 
                    self.state = 77
                    self._errHandler.sync(self)
                    _alt = self._interp.adaptivePredict(self._input,8,self._ctx)

                self.state = 78
                self.match(simbaParser.DEDENT)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





