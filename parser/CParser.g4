parser grammar CParser;
options { tokenVocab=CLexer; }

program : function+;


function : var_type ID LPAREN formal_args? RPAREN LBRACE statement* RBRACE;
    


var_type : INT_TYPE
    |   FLOAT_TYPE
    |   CHAR_TYPE
    |   VOID_TYPE
    ;


formal_args : (var_type (MULTIPLY)? ID ( LBRACK (INT)? RBRACK)? ) (COMMA var_type (MULTIPLY)? ID ( LBRACK (INT)? RBRACK)? )*;


actual_args : (eval_expr) ( COMMA eval_expr)*;


statement : declare_var_statm SEMI
    | assign_statm SEMI
    | return_statm SEMI
    | call_func_statm SEMI  
    | condition_statm 
    | while_statm
    | for_statm
    | arith_statm SEMI
    ;

    

/**
 * Here is the detail statement type
 */

return_statm : RET
    |       RET ( eval_expr )
    ;

declare_var_statm : var_type (MULTIPLY)? ID
    |       var_type (MULTIPLY)? ID LBRACK ( eval_expr ) RBRACK // this is the array:  int a[200];
    |       var_type (MULTIPLY)? ID ASSIGN ( eval_expr ) 
    ;

assign_statm : eval_expr ASSIGN ( eval_expr );

call_func_statm : ID LPAREN ( actual_args? ) RPAREN;


condition_statm : IF LPAREN ( eval_expr ) RPAREN LBRACE statement* RBRACE
    ( ELSE IF LPAREN ( eval_expr ) RPAREN LBRACE statement* RBRACE )*
    ( ELSE LBRACE statement* RBRACE )?
    ;

while_statm : WHILE LPAREN ( eval_expr ) RPAREN 
    LBRACE 
        statement* 
    RBRACE;

//for (int i = 0; i < n - 1; i++)
for_statm : FOR LPAREN ( declare_var_statm | assign_statm )? SEMI eval_expr? SEMI ( assign_statm | arith_statm )? RPAREN 
    LBRACE
        statement*
    RBRACE;

arith_statm : 
        eval_expr SELF_INC                                         // a++;
    |   eval_expr SELF_DEC                                         // b--;

    |   SELF_INC eval_expr                                         // ++a
    |   SELF_DEC eval_expr                                         // --a

    |   eval_expr SHL eval_expr                                    // a << (b+c)
    |   eval_expr SHR eval_expr                                    // a >> (b+c)
    ;


/**
 * statement type end
 */










const_val : INT
    |       FLOAT
    |       CHAR
    |       STRING
    |       ESCAPE_CHAR
    ;

// sign priority reference: https://c.biancheng.net/view/285.html
eval_expr : ID LBRACK eval_expr RBRACK                      // array[a+b]
    |   ID LPAREN ( actual_args? ) RPAREN                   // func(a, b)
    |   eval_expr SELF_INC                                         // a++;
    |   eval_expr SELF_DEC                                         // b--;

    |   SELF_INC eval_expr                                        // ++a
    |   SELF_DEC eval_expr                                         // --a
    |   NOT eval_expr                                             // this is !a 

    |   MULTIPLY eval_expr                                          // *a
    |   OP_AND eval_expr                                            // &a
    |   SIZEOF LPAREN ( var_type | eval_expr ) RPAREN              // sizeof(a) | sizeof(int)

    |   eval_expr ( MULTIPLY | DIVIDE | MODULO ) eval_expr  // * / %
    |   eval_expr ( PLUS | MINUS ) eval_expr                // + -

    |   eval_expr SHL eval_expr                                    // a << (b+c)
    |   eval_expr SHR eval_expr                                    // a >> (b+c)

    |   eval_expr GREATER eval_expr                         // a > c
    |   eval_expr GREATER_EQUAL eval_expr                   // a >= c
    |   eval_expr LESS eval_expr                            // a < c
    |   eval_expr LESS_EQUAL eval_expr                      // a <= c 
    |   eval_expr EQUAL eval_expr                           // a == b
    |   eval_expr NOT_EQUAL eval_expr                       // a != builtin_oper

    |   eval_expr OP_AND eval_expr                          // a & b, a ^ b, a | b
    |   eval_expr OP_XOR eval_expr
    |   eval_expr OP_OR eval_expr

    |   eval_expr AND eval_expr                             // a && b
    |   eval_expr OR eval_expr                              // a || b

    |   eval_expr ASSIGN eval_expr                                 // a = b = c



    |   (ID | const_val) 

    |   LPAREN eval_expr RPAREN                             // ( a + b ) * c

    ;


