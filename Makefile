define pre-flex-yacc
    @flex -o ./tmp/lex.yy.c ./src/lexer.l
	@yacc -d -b ./tmp/y ./src/parser.y
	@cp ./src/main.c ./tmp/main.c
	@cp ./src/token.h ./tmp/token.h
endef

lexer: ./src/lexer.l ./src/parser.y ./src/main.c
	$(call pre-flex-yacc)
	@gcc -o ./bin/lexer ./tmp/main.c ./tmp/y.tab.c ./tmp/lex.yy.c

parser: ./src/lexer.l ./src/parser.y ./src/main.c
	$(call pre-flex-yacc)
	@gcc -o ./bin/parser ./tmp/main.c ./tmp/y.tab.c ./tmp/lex.yy.c
