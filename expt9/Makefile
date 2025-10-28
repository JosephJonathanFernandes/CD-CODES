all: tac

tac: y.tab.c lex.yy.c
	@echo "Building tac..."
	gcc -o tac y.tab.c lex.yy.c -lfl

y.tab.c y.tab.h: grammar.y
	bison -d -y grammar.y

lex.yy.c: lexer.l y.tab.h
	flex lexer.l

clean:
	rm -f y.tab.c y.tab.h lex.yy.c tac y.output
