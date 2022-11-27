# Read and write

def get_code_with_lineNumber():
    code=[]
    with open("./code.txt") as f:
        for line in f:
            word_list = line.strip().split()
            code.append(word_list)
    return code

def get_word_from_file():
    code=[]
    with open("code.txt") as f:
        for line in f:
            word_list = line.strip().split()
            for word in word_list:
                code.append(word)
    return code

def push_out_tokens_into_file(tokens):
    with open("./result.txt", 'w') as f:
        for token in tokens:
            for order, type, value in token:
                f.write(str(order) + " " + type + " " + value)
                f.write('\n')
