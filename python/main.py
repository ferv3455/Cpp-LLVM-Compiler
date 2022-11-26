import argparse

from lexer import generateTokens
from lexrules import RULES


def main(args: argparse.Namespace) -> None:
    with open(args.input, "r") as fp:
        text = fp.read()
        tokens = generateTokens(text, RULES)

        if args.lex:
            # with open(args.output, "w") as fout:
            for token in tokens:
                print("{:24}{}".format(token.name, token.value))
            # print(token, file=fout)
            return


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='test')
    parser.add_argument('input', type=str, help='input source code')
    parser.add_argument('-o', '--output', type=str,
                        default='output', help='output file')
    parser.add_argument('-l', '--lex', action='store_true',
                        help='lexical analysis')
    # parser.add_argument('-p', '--parse', action='store_true', help='parsing')

    args = parser.parse_args()
    main(args)
