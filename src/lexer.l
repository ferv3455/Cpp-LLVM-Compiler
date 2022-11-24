%{
  #include "token.h"
  #include "y.tab.h"
  #include <stdio.h>
  #include <string.h>
%}

%option noyywrap

/* Regular Definitions (float not correct now) */
id          [A-Za-z_][A-Za-z_0-9]*
number      -?[0-9]+
float       -?[0-9]+\.[0-9]*
string      "\"".*"\""

%%
 /* ============= ADD TRANSLATION RULES BELOW ============= */

 /* Preprocessor directives */
^"#include"[[:space:]]*"<".+">" { printf("(include) %s\n", yytext); return INCLUDE; }
^"#define"[[:space:]]*{id}      { printf("(define) %s\n", yytext); return DEFINE; }

 /* Keywords */
 /*   Flow of control */
"return"                    { printf("(keyword) %s\n", yytext); return RETURN; }
"if"                        { printf("(keyword) %s\n", yytext); return IF; }
"else"                      { printf("(keyword) %s\n", yytext); return ELSE; }
"for"	                      { printf("(keyword) %s\n", yytext); return FOR; }
"while"                     { printf("(keyword) %s\n", yytext); return WHILE; }

 /*   Original data types */
"char"                      { printf("(type) char\n"); return CHAR; }
"int"                       { printf("(type) int\n"); return INT; }
"float"                     { printf("(type) float\n"); return FLOAT; }
"double"                    { printf("(type) double\n"); return DOUBLE; }
"void"                      { printf("(type) void\n"); return VOID; }

 /*   Boolean literals */
"true"                      { printf("(keyword) %s\n", yytext); return TRUE; }
"false"                     { printf("(keyword) %s\n", yytext); return FALSE; }

 /* Delimiters */
"("                         { printf("(delim) left-paren\n"); return LEFT_PAREN; }
")"                         { printf("(delim) right-paren\n"); return RIGHT_PAREN; }
"["                         { printf("(delim) left-bracket\n"); return LEFT_BRACKET; }
"]"                         { printf("(delim) right-bracket\n"); return RIGHT_BRACKET; }
"{"                         { printf("(delim) left-brace\n"); return LEFT_BRACE; }
"}"                         { printf("(delim) right-brace\n"); return RIGHT_BRACE; }
";"                         { printf("(delim) semicolon\n"); return SEMICOLON; }
","                         { printf("(delim) comma\n"); return COMMA; }
"."                         { printf("(delim) dot\n"); return DOT; }
"->"                        { printf("(delim) pointer\n"); return POINTER; }
"::"                        { printf("(delim) double-colon\n"); return DB_COLON; }

 /* Operators */
 /*   Calculation */
[-+*/%^=&\|]                { yylval.char_val = yytext[0]; printf("(op) %s\n", yytext); return BIN_OP; }
("--")|("++")               { yylval.char_val = yytext[0]; printf("(unary) %s\n", yytext); return UN_OP; }

 /*   Relation */
">"                         { yylval.char_val = GT; printf("(relop) %s\n", yytext); return REL_OP; }
">="                        { yylval.char_val = GE; printf("(relop) %s\n", yytext); return REL_OP; }
"=="                        { yylval.char_val = EQ; printf("(relop) %s\n", yytext); return REL_OP; }
"!="                        { yylval.char_val = NE; printf("(relop) %s\n", yytext); return REL_OP; }
"<="                        { yylval.char_val = LE; printf("(relop) %s\n", yytext); return REL_OP; }
"<"                         { yylval.char_val = LT; printf("(relop) %s\n", yytext); return REL_OP; }

 /*   Logic */
"&&"|"||"                   { yylval.char_val = yytext[0]; printf("(logic) %s\n", yytext); return LOG_OP; }

 /* Identifiers and literals */
{id}                        { printf("(id) \"%s\"\n", yytext); return ID; }
{number}                    { yylval.int_val = atoi(yytext); printf("(literal) %d\n", yylval.int_val); return INT_LIT; }
{float}                     { yylval.double_val = atof(yytext); printf("(literal) %f\n", yylval.double_val); return FLOAT_LIT; }
{string}                    { yylval.str_val = strdup(yytext); printf("(literal) %s\n", yylval.str_val); return STR_LIT; }

 /* Ignore comments and whitespace */
\/\/[^\n]*                  ;
[ \t\r\n]                   ;

 /* Unknown tokens */
.                           { printf("(unknown) \"%s\"\n", yytext); return UNKNOWN; }

 /* End of file */
<<EOF>>                     { printf("(eof) \n"); return 0; }

%%

/* ============= LINES BELOW SHOULD NOT BE EDITED NOW ============= */

int lex(FILE *file) {
  yyin = file;
  return yylex();
}
