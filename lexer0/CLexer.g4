lexer grammar CLexer;

// Include libs 
PREPROCESSOR_DIRECTIVE: '#' ~[\r\n]* '\r'? '\n' -> skip;


// Tokens
ID          : [a-zA-Z_][a-zA-Z0-9_]*; // Identifier
INT         : '0' | [1-9][0-9]*;      // Integer constant
FLOAT       : [0-9]+ '.' [0-9]*;      // Floating-point constant
CHAR        : '\'' . '\'';            // Character constant
ESCAPE_CHAR : '\'' '\\' ('n' | '0' | 'r' | 't' | 'f') '\''; // escape char constant 
STRING      : '"' .*? '"';            // String constant



// Arithmetic Operators
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

// Address Operators 
ADDRESS_OF  : '&'; 

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
