/* A Bison parser, made by GNU Bison 3.5.1.  */

/* Bison interface for Yacc-like parsers in C

   Copyright (C) 1984, 1989-1990, 2000-2015, 2018-2020 Free Software Foundation,
   Inc.

   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <http://www.gnu.org/licenses/>.  */

/* As a special exception, you may create a larger work that contains
   part or all of the Bison parser skeleton and distribute that work
   under terms of your choice, so long as that work isn't itself a
   parser generator using the skeleton or a modified version thereof
   as a parser skeleton.  Alternatively, if you modify or redistribute
   the parser skeleton itself, you may (at your option) remove this
   special exception, which will cause the skeleton and the resulting
   Bison output files to be licensed under the GNU General Public
   License without this special exception.

   This special exception was added by the Free Software Foundation in
   version 2.2 of Bison.  */

/* Undocumented macros, especially those whose name start with YY_,
   are private implementation details.  Do not rely on them.  */

#ifndef YY_YY_TMP_Y_TAB_H_INCLUDED
# define YY_YY_TMP_Y_TAB_H_INCLUDED
/* Debug traces.  */
#ifndef YYDEBUG
# define YYDEBUG 0
#endif
#if YYDEBUG
extern int yydebug;
#endif

/* Token type.  */
#ifndef YYTOKENTYPE
# define YYTOKENTYPE
  enum yytokentype
  {
    INCLUDE = 258,
    DEFINE = 259,
    RETURN = 260,
    IF = 261,
    ELSE = 262,
    FOR = 263,
    WHILE = 264,
    INT = 265,
    FLOAT = 266,
    DOUBLE = 267,
    CHAR = 268,
    VOID = 269,
    TRUE = 270,
    FALSE = 271,
    LEFT_PAREN = 272,
    RIGHT_PAREN = 273,
    LEFT_BRACKET = 274,
    RIGHT_BRACKET = 275,
    LEFT_BRACE = 276,
    RIGHT_BRACE = 277,
    SEMICOLON = 278,
    COMMA = 279,
    DOT = 280,
    POINTER = 281,
    DB_COLON = 282,
    BIN_OP = 283,
    UN_OP = 284,
    REL_OP = 285,
    LOG_OP = 286,
    ID = 287,
    INT_LIT = 288,
    FLOAT_LIT = 289,
    STR_LIT = 290,
    UNKNOWN = 291
  };
#endif
/* Tokens.  */
#define INCLUDE 258
#define DEFINE 259
#define RETURN 260
#define IF 261
#define ELSE 262
#define FOR 263
#define WHILE 264
#define INT 265
#define FLOAT 266
#define DOUBLE 267
#define CHAR 268
#define VOID 269
#define TRUE 270
#define FALSE 271
#define LEFT_PAREN 272
#define RIGHT_PAREN 273
#define LEFT_BRACKET 274
#define RIGHT_BRACKET 275
#define LEFT_BRACE 276
#define RIGHT_BRACE 277
#define SEMICOLON 278
#define COMMA 279
#define DOT 280
#define POINTER 281
#define DB_COLON 282
#define BIN_OP 283
#define UN_OP 284
#define REL_OP 285
#define LOG_OP 286
#define ID 287
#define INT_LIT 288
#define FLOAT_LIT 289
#define STR_LIT 290
#define UNKNOWN 291

/* Value type.  */
#if ! defined YYSTYPE && ! defined YYSTYPE_IS_DECLARED
union YYSTYPE
{
#line 9 "./src/parser.y"

	char char_val;
	int int_val;
    float float_val;
    double double_val;
    char *str_val;

#line 137 "./tmp/y.tab.h"

};
typedef union YYSTYPE YYSTYPE;
# define YYSTYPE_IS_TRIVIAL 1
# define YYSTYPE_IS_DECLARED 1
#endif


extern YYSTYPE yylval;

int yyparse (void);

#endif /* !YY_YY_TMP_Y_TAB_H_INCLUDED  */
