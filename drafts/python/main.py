# state changing and recognizing

import tokenList
import readwrite

token_list = {'origin': 0, 'reserved': 1, 'operator': 2, 'delimiter': 3, 'literal': 4, 'include&define': 5, 'identifier': 6, 'error': 7, 'comment': 8}

code_list=[]
output_token_list = []

state = 0
start = 0

def reco_token(word, line_number):
    state = 0
    start = 0
    while True:
        match state: # similar to switch in C
            case 0:
                if word[start] == '#':
                    state = 5
                    start += 1
                elif word in tokenList.op:
                    state = 2
                    start += 1
                elif word in tokenList.delim:
                    state = 3
                    start += 1
                elif word[start] in tokenList.constant:
                    state = 4
                    start += 1
                elif word[start] in tokenList.alphabet:
                    if word in tokenList.reserved:
                        state = 1
                        start += 1
                    else:
                        state = 6
                        start += 1
                elif word[start] == '/':
                    state = 8
                    start += 1
                else:
                    state = 7
                    start += 1
                continue
            case 1:
                return token_list['reserved'], 'reserved', word
            case 2:
                return token_list['operator'], 'operator', word
            case 3:
                return token_list['delimiter'], 'delimiter', word
            case 4:
                if start == len(word):
                    return token_list['literal'], 'literal', word
                elif word[start] in tokenList.constant:
                    start += 1
                else:
                    state = 7
                    start += 1
                continue
            case 5:
                if word == '#include':
                    return token_list['include&define'], 'include', word
                elif word == '#define':
                    return token_list['include&define'], 'define', word
                else:
                    state = 7
                    start += 1
                continue
            case 6:
                if start == len(word):
                    return token_list['identifier'], 'identifier', word
                elif word[start] in tokenList.alphabet or word[start] in tokenList.constant:
                    start += 1
                else:
                    state = 7
                    start += 1
                continue
            case 7:
                return token_list['error'], 'error', word
            case 8:
                if word[start] == '/':
                    return token_list['comment'], 'comment', word
                else:
                    state = 7
                    start += 1
                continue
    return token_list['error'], 'error', word

def main():
    code_list = readwrite.get_code_with_lineNumber()
    line_number = 0

    for line in code_list:
        line_number += 1
        for word in line:
            token = reco_token(word, line_number)
            output_token_list.append(token)

    for token in output_token_list:
        print(token)
    return

if __name__ == "__main__":
    main()