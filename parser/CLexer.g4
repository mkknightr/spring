lexer grammar CLexer;

// Include libs 
PREPROCESSOR_DIRECTIVE: '#' ~[\r\n]* '\r'? '\n' -> skip;







// Arithmetic Operators
SELF_INC    : '++';
SELF_DEC    : '--';
PLUS        : '+';
MINUS       : '-';
MULTIPLY    : '*';
DIVIDE      : '/';
MODULO      : '%';
ASSIGN      : '=';



// Logical Operators 
EQUAL       : '==';
NOT_EQUAL   : '!=';
LESS        : '<';
LESS_EQUAL  : '<=';
GREATER     : '>';
GREATER_EQUAL: '>=';
AND         : '&&';
OR          : '||';
NOT         : '!';

// bit level operators
REVERSE     : '~';
OP_AND      : '&';
OP_XOR      : '^';
OP_OR       : '|';
SHL         : '<<';
SHR         : '>>';

// Delimiters
SEMI        : ';';
COMMA       : ',';
LPAREN      : '(';
RPAREN      : ')';
LBRACE      : '{';
RBRACE      : '}';
LBRACK      : '[';
RBRACK      : ']';

// Whitespace and comments
WS          : [ \t\r\n]+ -> skip;    // Skip whitespace
BLOCK_COMMENT     : '/*' .*? '*/' -> skip; // Skip comments
LINE_COMMENT: '//' ~[\r\n]* -> skip; // Skip line comments


//Here is the variable type
INT_TYPE    : 'int';
FLOAT_TYPE  : 'float';
CHAR_TYPE   : 'char';
VOID_TYPE   : 'void';


//control reserved word
RET         : 'return';
IF          : 'if';
ELSE        : 'else';
WHILE       : 'while';
FOR         : 'for';


//builtin operator
SIZEOF      : 'sizeof';



// Tokens
// ! ID has to be put into the last place for it would match other keyword like "return"
// ! specific keywords like return are listed in the lexer rules before the general ID rule
ID          : [a-zA-Z_][a-zA-Z0-9_]*; // Identifier
INT         : '0' | [1-9][0-9]*;      // Integer constant
FLOAT       : [0-9]+ '.' [0-9]*;      // Floating-point constant
CHAR        : '\'' . '\'';            // Character constant
ESCAPE_CHAR : '\'' '\\' ('n' | '0' | 'r' | 't' | 'f') '\''; // escape char constant 
STRING      : '"' .*? '"';            // String constant