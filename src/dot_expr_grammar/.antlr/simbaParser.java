// Generated from /Users/jeremievaney/Desktop/language/grammar/simba.g4 by ANTLR 4.8
import org.antlr.v4.runtime.atn.*;
import org.antlr.v4.runtime.dfa.DFA;
import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.misc.*;
import org.antlr.v4.runtime.tree.*;
import java.util.List;
import java.util.Iterator;
import java.util.ArrayList;

@SuppressWarnings({"all", "warnings", "unchecked", "unused", "cast"})
public class simbaParser extends Parser {
	static { RuntimeMetaData.checkVersion("4.8", RuntimeMetaData.VERSION); }

	protected static final DFA[] _decisionToDFA;
	protected static final PredictionContextCache _sharedContextCache =
		new PredictionContextCache();
	public static final int
		T__0=1, LITERAL=2, STRING=3, NAME=4, OPERATOR=5, INDENT=6, DEDENT=7, WS=8, 
		TAB=9, NUMBER=10, LPAREN=11, RPAREN=12, LSSQUARE=13, RSSQUARE=14, LCURLY=15, 
		RCURLY=16;
	public static final int
		RULE_start = 0, RULE_form = 1, RULE_sequence = 2, RULE_association = 3, 
		RULE_comment = 4;
	private static String[] makeRuleNames() {
		return new String[] {
			"start", "form", "sequence", "association", "comment"
		};
	}
	public static final String[] ruleNames = makeRuleNames();

	private static String[] makeLiteralNames() {
		return new String[] {
			null, "';'", null, null, null, null, "'>'", "'<'", null, "'\t'", null, 
			"'('", "')'", "'['", "']'", "'{'", "'}'"
		};
	}
	private static final String[] _LITERAL_NAMES = makeLiteralNames();
	private static String[] makeSymbolicNames() {
		return new String[] {
			null, null, "LITERAL", "STRING", "NAME", "OPERATOR", "INDENT", "DEDENT", 
			"WS", "TAB", "NUMBER", "LPAREN", "RPAREN", "LSSQUARE", "RSSQUARE", "LCURLY", 
			"RCURLY"
		};
	}
	private static final String[] _SYMBOLIC_NAMES = makeSymbolicNames();
	public static final Vocabulary VOCABULARY = new VocabularyImpl(_LITERAL_NAMES, _SYMBOLIC_NAMES);

	/**
	 * @deprecated Use {@link #VOCABULARY} instead.
	 */
	@Deprecated
	public static final String[] tokenNames;
	static {
		tokenNames = new String[_SYMBOLIC_NAMES.length];
		for (int i = 0; i < tokenNames.length; i++) {
			tokenNames[i] = VOCABULARY.getLiteralName(i);
			if (tokenNames[i] == null) {
				tokenNames[i] = VOCABULARY.getSymbolicName(i);
			}

			if (tokenNames[i] == null) {
				tokenNames[i] = "<INVALID>";
			}
		}
	}

	@Override
	@Deprecated
	public String[] getTokenNames() {
		return tokenNames;
	}

	@Override

	public Vocabulary getVocabulary() {
		return VOCABULARY;
	}

	@Override
	public String getGrammarFileName() { return "simba.g4"; }

	@Override
	public String[] getRuleNames() { return ruleNames; }

	@Override
	public String getSerializedATN() { return _serializedATN; }

	@Override
	public ATN getATN() { return _ATN; }

	public simbaParser(TokenStream input) {
		super(input);
		_interp = new ParserATNSimulator(this,_ATN,_decisionToDFA,_sharedContextCache);
	}

	public static class StartContext extends ParserRuleContext {
		public TerminalNode EOF() { return getToken(simbaParser.EOF, 0); }
		public List<FormContext> form() {
			return getRuleContexts(FormContext.class);
		}
		public FormContext form(int i) {
			return getRuleContext(FormContext.class,i);
		}
		public StartContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_start; }
	}

	public final StartContext start() throws RecognitionException {
		StartContext _localctx = new StartContext(_ctx, getState());
		enterRule(_localctx, 0, RULE_start);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(13);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while ((((_la) & ~0x3f) == 0 && ((1L << _la) & ((1L << LITERAL) | (1L << OPERATOR) | (1L << LPAREN) | (1L << LSSQUARE) | (1L << LCURLY))) != 0)) {
				{
				{
				setState(10);
				form();
				}
				}
				setState(15);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			setState(16);
			match(EOF);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class FormContext extends ParserRuleContext {
		public TerminalNode LITERAL() { return getToken(simbaParser.LITERAL, 0); }
		public SequenceContext sequence() {
			return getRuleContext(SequenceContext.class,0);
		}
		public AssociationContext association() {
			return getRuleContext(AssociationContext.class,0);
		}
		public TerminalNode OPERATOR() { return getToken(simbaParser.OPERATOR, 0); }
		public List<FormContext> form() {
			return getRuleContexts(FormContext.class);
		}
		public FormContext form(int i) {
			return getRuleContext(FormContext.class,i);
		}
		public TerminalNode INDENT() { return getToken(simbaParser.INDENT, 0); }
		public TerminalNode DEDENT() { return getToken(simbaParser.DEDENT, 0); }
		public TerminalNode LPAREN() { return getToken(simbaParser.LPAREN, 0); }
		public TerminalNode RPAREN() { return getToken(simbaParser.RPAREN, 0); }
		public FormContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_form; }
	}

	public final FormContext form() throws RecognitionException {
		FormContext _localctx = new FormContext(_ctx, getState());
		enterRule(_localctx, 2, RULE_form);
		int _la;
		try {
			int _alt;
			setState(42);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case LITERAL:
				enterOuterAlt(_localctx, 1);
				{
				setState(18);
				match(LITERAL);
				}
				break;
			case LSSQUARE:
				enterOuterAlt(_localctx, 2);
				{
				setState(19);
				sequence();
				}
				break;
			case LCURLY:
				enterOuterAlt(_localctx, 3);
				{
				setState(20);
				association();
				}
				break;
			case OPERATOR:
				enterOuterAlt(_localctx, 4);
				{
				setState(21);
				match(OPERATOR);
				setState(25);
				_errHandler.sync(this);
				_alt = getInterpreter().adaptivePredict(_input,1,_ctx);
				while ( _alt!=2 && _alt!=org.antlr.v4.runtime.atn.ATN.INVALID_ALT_NUMBER ) {
					if ( _alt==1 ) {
						{
						{
						setState(22);
						form();
						}
						} 
					}
					setState(27);
					_errHandler.sync(this);
					_alt = getInterpreter().adaptivePredict(_input,1,_ctx);
				}
				setState(36);
				_errHandler.sync(this);
				switch ( getInterpreter().adaptivePredict(_input,3,_ctx) ) {
				case 1:
					{
					setState(28);
					match(INDENT);
					setState(32);
					_errHandler.sync(this);
					_la = _input.LA(1);
					while ((((_la) & ~0x3f) == 0 && ((1L << _la) & ((1L << LITERAL) | (1L << OPERATOR) | (1L << LPAREN) | (1L << LSSQUARE) | (1L << LCURLY))) != 0)) {
						{
						{
						setState(29);
						form();
						}
						}
						setState(34);
						_errHandler.sync(this);
						_la = _input.LA(1);
					}
					setState(35);
					match(DEDENT);
					}
					break;
				}
				}
				break;
			case LPAREN:
				enterOuterAlt(_localctx, 5);
				{
				setState(38);
				match(LPAREN);
				setState(39);
				form();
				setState(40);
				match(RPAREN);
				}
				break;
			default:
				throw new NoViableAltException(this);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class SequenceContext extends ParserRuleContext {
		public TerminalNode LSSQUARE() { return getToken(simbaParser.LSSQUARE, 0); }
		public TerminalNode RSSQUARE() { return getToken(simbaParser.RSSQUARE, 0); }
		public List<FormContext> form() {
			return getRuleContexts(FormContext.class);
		}
		public FormContext form(int i) {
			return getRuleContext(FormContext.class,i);
		}
		public SequenceContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_sequence; }
	}

	public final SequenceContext sequence() throws RecognitionException {
		SequenceContext _localctx = new SequenceContext(_ctx, getState());
		enterRule(_localctx, 4, RULE_sequence);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(44);
			match(LSSQUARE);
			setState(48);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while ((((_la) & ~0x3f) == 0 && ((1L << _la) & ((1L << LITERAL) | (1L << OPERATOR) | (1L << LPAREN) | (1L << LSSQUARE) | (1L << LCURLY))) != 0)) {
				{
				{
				setState(45);
				form();
				}
				}
				setState(50);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			setState(51);
			match(RSSQUARE);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class AssociationContext extends ParserRuleContext {
		public TerminalNode LCURLY() { return getToken(simbaParser.LCURLY, 0); }
		public TerminalNode RCURLY() { return getToken(simbaParser.RCURLY, 0); }
		public List<FormContext> form() {
			return getRuleContexts(FormContext.class);
		}
		public FormContext form(int i) {
			return getRuleContext(FormContext.class,i);
		}
		public AssociationContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_association; }
	}

	public final AssociationContext association() throws RecognitionException {
		AssociationContext _localctx = new AssociationContext(_ctx, getState());
		enterRule(_localctx, 6, RULE_association);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(53);
			match(LCURLY);
			setState(59);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while ((((_la) & ~0x3f) == 0 && ((1L << _la) & ((1L << LITERAL) | (1L << OPERATOR) | (1L << LPAREN) | (1L << LSSQUARE) | (1L << LCURLY))) != 0)) {
				{
				{
				setState(54);
				form();
				setState(55);
				form();
				}
				}
				setState(61);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			setState(62);
			match(RCURLY);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class CommentContext extends ParserRuleContext {
		public TerminalNode INDENT() { return getToken(simbaParser.INDENT, 0); }
		public TerminalNode DEDENT() { return getToken(simbaParser.DEDENT, 0); }
		public CommentContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_comment; }
	}

	public final CommentContext comment() throws RecognitionException {
		CommentContext _localctx = new CommentContext(_ctx, getState());
		enterRule(_localctx, 8, RULE_comment);
		int _la;
		try {
			int _alt;
			enterOuterAlt(_localctx, 1);
			{
			setState(64);
			match(T__0);
			setState(68);
			_errHandler.sync(this);
			_alt = getInterpreter().adaptivePredict(_input,7,_ctx);
			while ( _alt!=1 && _alt!=org.antlr.v4.runtime.atn.ATN.INVALID_ALT_NUMBER ) {
				if ( _alt==1+1 ) {
					{
					{
					setState(65);
					matchWildcard();
					}
					} 
				}
				setState(70);
				_errHandler.sync(this);
				_alt = getInterpreter().adaptivePredict(_input,7,_ctx);
			}
			setState(79);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==INDENT) {
				{
				setState(71);
				match(INDENT);
				setState(75);
				_errHandler.sync(this);
				_alt = getInterpreter().adaptivePredict(_input,8,_ctx);
				while ( _alt!=1 && _alt!=org.antlr.v4.runtime.atn.ATN.INVALID_ALT_NUMBER ) {
					if ( _alt==1+1 ) {
						{
						{
						setState(72);
						matchWildcard();
						}
						} 
					}
					setState(77);
					_errHandler.sync(this);
					_alt = getInterpreter().adaptivePredict(_input,8,_ctx);
				}
				setState(78);
				match(DEDENT);
				}
			}

			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static final String _serializedATN =
		"\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3\22T\4\2\t\2\4\3\t"+
		"\3\4\4\t\4\4\5\t\5\4\6\t\6\3\2\7\2\16\n\2\f\2\16\2\21\13\2\3\2\3\2\3\3"+
		"\3\3\3\3\3\3\3\3\7\3\32\n\3\f\3\16\3\35\13\3\3\3\3\3\7\3!\n\3\f\3\16\3"+
		"$\13\3\3\3\5\3\'\n\3\3\3\3\3\3\3\3\3\5\3-\n\3\3\4\3\4\7\4\61\n\4\f\4\16"+
		"\4\64\13\4\3\4\3\4\3\5\3\5\3\5\3\5\7\5<\n\5\f\5\16\5?\13\5\3\5\3\5\3\6"+
		"\3\6\7\6E\n\6\f\6\16\6H\13\6\3\6\3\6\7\6L\n\6\f\6\16\6O\13\6\3\6\5\6R"+
		"\n\6\3\6\4FM\2\7\2\4\6\b\n\2\2\2[\2\17\3\2\2\2\4,\3\2\2\2\6.\3\2\2\2\b"+
		"\67\3\2\2\2\nB\3\2\2\2\f\16\5\4\3\2\r\f\3\2\2\2\16\21\3\2\2\2\17\r\3\2"+
		"\2\2\17\20\3\2\2\2\20\22\3\2\2\2\21\17\3\2\2\2\22\23\7\2\2\3\23\3\3\2"+
		"\2\2\24-\7\4\2\2\25-\5\6\4\2\26-\5\b\5\2\27\33\7\7\2\2\30\32\5\4\3\2\31"+
		"\30\3\2\2\2\32\35\3\2\2\2\33\31\3\2\2\2\33\34\3\2\2\2\34&\3\2\2\2\35\33"+
		"\3\2\2\2\36\"\7\b\2\2\37!\5\4\3\2 \37\3\2\2\2!$\3\2\2\2\" \3\2\2\2\"#"+
		"\3\2\2\2#%\3\2\2\2$\"\3\2\2\2%\'\7\t\2\2&\36\3\2\2\2&\'\3\2\2\2\'-\3\2"+
		"\2\2()\7\r\2\2)*\5\4\3\2*+\7\16\2\2+-\3\2\2\2,\24\3\2\2\2,\25\3\2\2\2"+
		",\26\3\2\2\2,\27\3\2\2\2,(\3\2\2\2-\5\3\2\2\2.\62\7\17\2\2/\61\5\4\3\2"+
		"\60/\3\2\2\2\61\64\3\2\2\2\62\60\3\2\2\2\62\63\3\2\2\2\63\65\3\2\2\2\64"+
		"\62\3\2\2\2\65\66\7\20\2\2\66\7\3\2\2\2\67=\7\21\2\289\5\4\3\29:\5\4\3"+
		"\2:<\3\2\2\2;8\3\2\2\2<?\3\2\2\2=;\3\2\2\2=>\3\2\2\2>@\3\2\2\2?=\3\2\2"+
		"\2@A\7\22\2\2A\t\3\2\2\2BF\7\3\2\2CE\13\2\2\2DC\3\2\2\2EH\3\2\2\2FG\3"+
		"\2\2\2FD\3\2\2\2GQ\3\2\2\2HF\3\2\2\2IM\7\b\2\2JL\13\2\2\2KJ\3\2\2\2LO"+
		"\3\2\2\2MN\3\2\2\2MK\3\2\2\2NP\3\2\2\2OM\3\2\2\2PR\7\t\2\2QI\3\2\2\2Q"+
		"R\3\2\2\2R\13\3\2\2\2\f\17\33\"&,\62=FMQ";
	public static final ATN _ATN =
		new ATNDeserializer().deserialize(_serializedATN.toCharArray());
	static {
		_decisionToDFA = new DFA[_ATN.getNumberOfDecisions()];
		for (int i = 0; i < _ATN.getNumberOfDecisions(); i++) {
			_decisionToDFA[i] = new DFA(_ATN.getDecisionState(i), i);
		}
	}
}