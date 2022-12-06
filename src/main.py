import argparse

from mycompiler.lexer import generateTokens
from mycompiler.parser import generateAST

from rules import RULES, GRAMMAR


def main(args: argparse.Namespace) -> None:
    with open(args.input, "r") as fp:
        # Get source code
        text = fp.read()

        # Lexical analysis
        if args.update:
            tokens = generateTokens(text, RULES)
        else:
            tokens = generateTokens(text)
        if args.lex:
            with open(args.output, "w") as fout:
                for token in tokens:
                    print("{:24}{}".format(token.name, token.value))
                    print("{:24}{}".format(token.name, token.value), file=fout)
            return

        # Parsing
        if args.update:
            ast = generateAST(tokens, GRAMMAR)
        else:
            ast = generateAST(tokens)
        if args.parse:
            with open(args.output, "w") as fout:
                print(ast)
                print(ast, file=fout)
            return


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Cpp-LLVM Compiler')
    parser.add_argument('input', type=str, help='input source code')
    parser.add_argument('-o', '--output', type=str,
                        default='output', help='output file')
    parser.add_argument('-u', '--update', action='store_true',
                        help='rebuild all rules and grammar (update temporary files)')
    parser.add_argument('-l', '--lex', action='store_true',
                        help='lexical analysis')
    parser.add_argument('-p', '--parse', action='store_true', help='parsing')

    args = parser.parse_args()
    main(args)
