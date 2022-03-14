// Generated from /Users/jeremievaney/Desktop/language/grammar/simba.g4 by ANTLR 4.8
import org.antlr.v4.runtime.Lexer;
import org.antlr.v4.runtime.CharStream;
import org.antlr.v4.runtime.Token;
import org.antlr.v4.runtime.TokenStream;
import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.atn.*;
import org.antlr.v4.runtime.dfa.DFA;
import org.antlr.v4.runtime.misc.*;

@SuppressWarnings({"all", "warnings", "unchecked", "unused", "cast"})
public class simbaLexer extends Lexer {
	static { RuntimeMetaData.checkVersion("4.8", RuntimeMetaData.VERSION); }

	protected static final DFA[] _decisionToDFA;
	protected static final PredictionContextCache _sharedContextCache =
		new PredictionContextCache();
	public static final int
		T__0=1, LITERAL=2, STRING=3, NAME=4, OPERATOR=5, INDENT=6, DEDENT=7, WS=8, 
		TAB=9, NUMBER=10, LPAREN=11, RPAREN=12, LSSQUARE=13, RSSQUARE=14, LCURLY=15, 
		RCURLY=16;
	public static String[] channelNames = {
		"DEFAULT_TOKEN_CHANNEL", "HIDDEN"
	};

	public static String[] modeNames = {
		"DEFAULT_MODE"
	};

	private static String[] makeRuleNames() {
		return new String[] {
			"T__0", "LITERAL", "STRING", "STRING_ESCAPE_SEQ", "NAME", "OPERATOR", 
			"INDENT", "DEDENT", "WS", "TAB", "NUMBER", "LPAREN", "RPAREN", "LSSQUARE", 
			"RSSQUARE", "LCURLY", "RCURLY"
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


	public simbaLexer(CharStream input) {
		super(input);
		_interp = new LexerATNSimulator(this,_ATN,_decisionToDFA,_sharedContextCache);
	}

	@Override
	public String getGrammarFileName() { return "simba.g4"; }

	@Override
	public String[] getRuleNames() { return ruleNames; }

	@Override
	public String getSerializedATN() { return _serializedATN; }

	@Override
	public String[] getChannelNames() { return channelNames; }

	@Override
	public String[] getModeNames() { return modeNames; }

	@Override
	public ATN getATN() { return _ATN; }

	@Override
	public void action(RuleContext _localctx, int ruleIndex, int actionIndex) {
		switch (ruleIndex) {
		case 9:
			TAB_action((RuleContext)_localctx, actionIndex);
			break;
		}
	}
	private void TAB_action(RuleContext _localctx, int actionIndex) {
		switch (actionIndex) {
		case 0:
			 raise TabError('You should not use tabs in Simba source code.')  
			break;
		}
	}

	public static final String _serializedATN =
		"\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\2\22g\b\1\4\2\t\2\4"+
		"\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t"+
		"\13\4\f\t\f\4\r\t\r\4\16\t\16\4\17\t\17\4\20\t\20\4\21\t\21\4\22\t\22"+
		"\3\2\3\2\3\3\3\3\3\3\5\3+\n\3\3\4\3\4\3\4\7\4\60\n\4\f\4\16\4\63\13\4"+
		"\3\4\3\4\3\4\3\4\7\49\n\4\f\4\16\4<\13\4\3\4\5\4?\n\4\3\5\3\5\3\5\3\6"+
		"\6\6E\n\6\r\6\16\6F\3\7\3\7\3\7\3\b\3\b\3\t\3\t\3\n\3\n\3\n\3\n\3\13\3"+
		"\13\3\13\3\f\6\fX\n\f\r\f\16\fY\3\r\3\r\3\16\3\16\3\17\3\17\3\20\3\20"+
		"\3\21\3\21\3\22\3\22\2\2\23\3\3\5\4\7\5\t\2\13\6\r\7\17\b\21\t\23\n\25"+
		"\13\27\f\31\r\33\16\35\17\37\20!\21#\22\3\2\7\6\2\f\f\16\17))^^\6\2\f"+
		"\f\16\17$$^^\4\2C\\c|\5\2\f\f\17\17\"\"\3\2\62;\2n\2\3\3\2\2\2\2\5\3\2"+
		"\2\2\2\7\3\2\2\2\2\13\3\2\2\2\2\r\3\2\2\2\2\17\3\2\2\2\2\21\3\2\2\2\2"+
		"\23\3\2\2\2\2\25\3\2\2\2\2\27\3\2\2\2\2\31\3\2\2\2\2\33\3\2\2\2\2\35\3"+
		"\2\2\2\2\37\3\2\2\2\2!\3\2\2\2\2#\3\2\2\2\3%\3\2\2\2\5*\3\2\2\2\7>\3\2"+
		"\2\2\t@\3\2\2\2\13D\3\2\2\2\rH\3\2\2\2\17K\3\2\2\2\21M\3\2\2\2\23O\3\2"+
		"\2\2\25S\3\2\2\2\27W\3\2\2\2\31[\3\2\2\2\33]\3\2\2\2\35_\3\2\2\2\37a\3"+
		"\2\2\2!c\3\2\2\2#e\3\2\2\2%&\7=\2\2&\4\3\2\2\2\'+\5\13\6\2(+\5\27\f\2"+
		")+\5\7\4\2*\'\3\2\2\2*(\3\2\2\2*)\3\2\2\2+\6\3\2\2\2,\61\7)\2\2-\60\5"+
		"\t\5\2.\60\n\2\2\2/-\3\2\2\2/.\3\2\2\2\60\63\3\2\2\2\61/\3\2\2\2\61\62"+
		"\3\2\2\2\62\64\3\2\2\2\63\61\3\2\2\2\64?\7)\2\2\65:\7$\2\2\669\5\t\5\2"+
		"\679\n\3\2\28\66\3\2\2\28\67\3\2\2\29<\3\2\2\2:8\3\2\2\2:;\3\2\2\2;=\3"+
		"\2\2\2<:\3\2\2\2=?\7$\2\2>,\3\2\2\2>\65\3\2\2\2?\b\3\2\2\2@A\7^\2\2AB"+
		"\13\2\2\2B\n\3\2\2\2CE\t\4\2\2DC\3\2\2\2EF\3\2\2\2FD\3\2\2\2FG\3\2\2\2"+
		"G\f\3\2\2\2HI\5\13\6\2IJ\7\60\2\2J\16\3\2\2\2KL\7@\2\2L\20\3\2\2\2MN\7"+
		">\2\2N\22\3\2\2\2OP\t\5\2\2PQ\3\2\2\2QR\b\n\2\2R\24\3\2\2\2ST\7\13\2\2"+
		"TU\b\13\3\2U\26\3\2\2\2VX\t\6\2\2WV\3\2\2\2XY\3\2\2\2YW\3\2\2\2YZ\3\2"+
		"\2\2Z\30\3\2\2\2[\\\7*\2\2\\\32\3\2\2\2]^\7+\2\2^\34\3\2\2\2_`\7]\2\2"+
		"`\36\3\2\2\2ab\7_\2\2b \3\2\2\2cd\7}\2\2d\"\3\2\2\2ef\7\177\2\2f$\3\2"+
		"\2\2\13\2*/\618:>FY\4\b\2\2\3\13\2";
	public static final ATN _ATN =
		new ATNDeserializer().deserialize(_serializedATN.toCharArray());
	static {
		_decisionToDFA = new DFA[_ATN.getNumberOfDecisions()];
		for (int i = 0; i < _ATN.getNumberOfDecisions(); i++) {
			_decisionToDFA[i] = new DFA(_ATN.getDecisionState(i), i);
		}
	}
}