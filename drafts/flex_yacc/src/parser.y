%{
#include <stdio.h>
#include <stdlib.h>
extern int yylex(void);
extern void yyerror(const char *);
extern FILE *yyin;
%}

%union {
	char char_val;
	int int_val;
    float float_val;
    double double_val;
    char *str_val;
};

/* ============= ADD NEW TOKEN TYPES BELOW ============= */

/* Define Tokens Here */
/* Preprocessor directives */
%token INCLUDE DEFINE

/* Flow of control */
%token RETURN IF ELSE FOR WHILE

/* Original data types */
%token INT FLOAT DOUBLE CHAR VOID

/* Boolean literals */
%token TRUE FALSE

/* Delimiters */
%token LEFT_PAREN RIGHT_PAREN LEFT_BRACKET RIGHT_BRACKET LEFT_BRACE RIGHT_BRACE
%token SEMICOLON COMMA DOT POINTER DB_COLON

/* Operators */
%token <char_val> BIN_OP UN_OP REL_OP LOG_OP

/* Identifiers and literals */
%token ID
%token <int_val> INT_LIT 
%token <double_val> FLOAT_LIT
%token <str_val> STR_LIT CHAR_LIT

/* Unknown tokens */
%token UNKNOWN

/* ============= LINES BELOW SHOULD NOT BE EDITED NOW ============= */

/* Types of non-terminals */
%type <int_val> stm exp

%%
/* Define Grammars Here */
stm:    exp
        {
            printf("%d\n", $1);
        }
        ;

exp:    exp BIN_OP INT_LIT
        {
            if ($2 == '+') $$ = $1 + $3;
            else if ($2 == '-') $$ = $1 - $3;
            else if ($2 == '*') $$ = $1 * $3;
            else if ($2 == '/') $$ = $1 / $3;
        }
        | INT_LIT                 { $$ = $1; }
        ;

%%

void yyerror(const char *s)
{
    fprintf(stderr, "%s\n", s);
    exit(1);
}

int parse(FILE *file)
{
    yyin = file;
    return yyparse();
}
