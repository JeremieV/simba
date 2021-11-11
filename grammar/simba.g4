grammar simba;

start
    : form * EOF ;

form: LITERAL
    | sequence
    | association
    // | comment
    | OPERATOR form * (INDENT form * DEDENT)?
    | LPAREN form RPAREN
    ;

sequence: LSSQUARE form* RSSQUARE ;

association: LCURLY (form form)* RCURLY ;

comment : ';' .*? (INDENT .*? DEDENT)? ;

LITERAL
    : NAME
    | NUMBER 
    | STRING ;

STRING
 : '\'' ( STRING_ESCAPE_SEQ | ~[\\\r\n\f'] )* '\''
 | '"' ( STRING_ESCAPE_SEQ | ~[\\\r\n\f"] )* '"'
 ;

fragment STRING_ESCAPE_SEQ
 : '\\' .
//  | '\\' '\n'
 ;

NAME : [a-zA-Z]+ ;
OPERATOR : NAME '.' ;

INDENT : '>' ;
DEDENT : '<' ;

WS : [ \r\n] -> skip ;
TAB: '\t' { raise TabError('You should not use tabs in Simba source code.')  };
NUMBER  : [0-9]+ ;
LPAREN  : '(';
RPAREN  : ')';
LSSQUARE: '[';
RSSQUARE: ']';
LCURLY  : '{';
RCURLY  : '}';
// NL: ('\r'? '\n' ' '*) -> skip;


// // set_: '#{' forms '}' ;

// // reader_macro
// //     : lambda_
// //     | meta_data
// //     | regex
// //     | var_quote
// //     | host_expr
// //     | set_
// //     | tag
// //     | discard
// //     | dispatch
// //     | deref
// //     | quote
// //     | backtick
// //     | unquote
// //     | unquote_splicing
// //     | gensym
// //     ;

// // // TJP added '&' (gather a variable number of arguments)
// // quote
// //     : '\'' form
// //     ;

// // backtick
// //     : '`' form
// //     ;

// // unquote
// //     : '~' form
// //     ;

// // unquote_splicing
// //     : '~@' form
// //     ;

// // tag
// //     : '^' form form
// //     ;

// // deref
// //     : '@' form
// //     ;

// // gensym
// //     : SYMBOL '#'
// //     ;

// // lambda_
// //     : '#(' form* ')'
// //     ;

// // meta_data
// //     : '#^' (map_ form | form)
// //     ;

// // var_quote
// //     : '#\'' symbol
// //     ;

// // host_expr
// //     : '#+' form form
// //     ;

// // discard
// //     : '#_' form
// //     ;

// // dispatch
// //     : '#' symbol form
// //     ;

// // regex
// //     : '#' string_
// //     ;

// literal
//     : string_
//     | number
//     | character
//     | nil_
//     | BOOLEAN
//     // | keyword
//     | symbol
//     // | param_name
//     ;

// string_: STRING;
// hex_: HEX;
// bin_: BIN;
// bign: BIGN;
// number
//     : FLOAT
//     | hex_
//     | bin_
//     | bign
//     | LONG
//     ;

// character
//     : named_char
//     | u_hex_quad
//     | any_char
//     ;
// named_char: CHAR_NAMED ;
// any_char: CHAR_ANY ;
// u_hex_quad: CHAR_U ;

// nil_: NIL;

// // keyword: macro_keyword | simple_keyword;
// // simple_keyword: ':' symbol;
// // macro_keyword: ':' ':' symbol;

// symbol: ns_symbol | simple_sym;
// simple_sym: SYMBOL;
// ns_symbol: NS_SYMBOL;

// // param_name: PARAM_NAME;

// // Lexers
// //--------------------------------------------------------------------

// STRING : '"' ( ~'"' | '\\' '"' )* '"' ;

// // FIXME: Doesn't deal with arbitrary read radixes, BigNums
// FLOAT
//     : '-'? [0-9]+ FLOAT_TAIL
//     | '-'? 'Infinity'
//     | '-'? 'NaN'
//     ;

// // fragment
// FLOAT_TAIL
//     : FLOAT_DECIMAL FLOAT_EXP
//     | FLOAT_DECIMAL
//     | FLOAT_EXP
//     ;

// // fragment
// FLOAT_DECIMAL
//     : '.' [0-9]+
//     ;

// // fragment
// FLOAT_EXP
//     : [eE] '-'? [0-9]+
//     ;
// // fragment
// HEXD: [0-9a-fA-F] ;
// HEX: '0' [xX] HEXD+ ;
// BIN: '0' [bB] [10]+ ;
// LONG: '-'? [0-9]+[lL]?;
// BIGN: '-'? [0-9]+[nN];

// CHAR_U
//     : '\\' 'u'[0-9D-Fd-f] HEXD HEXD HEXD ;
// CHAR_NAMED
//     : '\\' ( 'newline'
//            | 'return'
//            | 'space'
//            | 'tab'
//            | 'formfeed'
//            | 'backspace' ) ;
// CHAR_ANY
//     : '\\' . ;

// NIL : 'nil';

// BOOLEAN : 'true' | 'false' ;

// SYMBOL
//     : '.'
//     | '/'
//     // | NAME
//     | [a-zA-Z]+
//     ;

// NS_SYMBOL
//     : NAME '/' SYMBOL
//     ;

// // PARAM_NAME: '%' ((('1'..'9')('0'..'9')*)|'&')? ;

// // // Fragments
// // //--------------------------------------------------------------------

// // fragment
// NAME: SYMBOL_HEAD SYMBOL_REST* (':' SYMBOL_REST+)* ;

// // fragment
// SYMBOL_HEAD
//     : ~('0' .. '9'
//         | '^' | '`' | '\'' | '"' | '#' | '~' | '@' | ':' | '/' | '%' | '(' | ')' | '[' | ']' | '{' | '}' // FIXME: could be one group
//         | [ \n\r\t,] // FIXME: could be WS
//         )
//     ;

// // fragment
// SYMBOL_REST
//     : SYMBOL_HEAD
//     | '0'..'9'
//     // | '.'
//     ;

// // Discard
// //--------------------------------------------------------------------

// // fragment
// WS : [ \n\r\t,] ;

// // fragment
// COMMENT: ';' ~[\r\n]* ;

// TRASH
//     : ( WS | COMMENT ) -> channel(HIDDEN)
//     ;
