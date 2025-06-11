#! /usr/bin/python3


# 数字の羅列を数に変換する関数
# line: [3, ., 0, +, 8], index: 0 → token: (NUMBER, 3.0), index: 3
def read_number(line, index):
    number = 0
    while index < len(line) and line[index].isdigit(): # 数字だったら
        number = number * 10 + int(line[index])
        index += 1
    if index < len(line) and line[index] == '.': # 少数に対応
        index += 1
        decimal = 0.1
        while index < len(line) and line[index].isdigit():
            number += int(line[index]) * decimal
            decimal /= 10
            index += 1
    token = {'type': 'NUMBER', 'number': number}
    return token, index

# "+"を読み込む
def read_plus(line, index):
    token = {'type': 'PLUS'}
    return token, index + 1

# "-"を読み込む
def read_minus(line, index):
    token = {'type': 'MINUS'}
    return token, index + 1

# "*"を読み込む
def read_star(line, index):
    token = {'type': 'STAR'}
    return token, index + 1

# "/"を読み込む
def read_slash(line, index):
    token = {'type': 'SLASH'}
    return token, index + 1

# [3, ., 0, +, 8] → [(NUMBER, 3.0), (PLUS), (NUMBER, 8)]
def tokenize(line):
    tokens = []
    index = 0
    while index < len(line):
        if line[index].isdigit():
            (token, index) = read_number(line, index)
        elif line[index] == '+':
            (token, index) = read_plus(line, index)
        elif line[index] == '-':
            (token, index) = read_minus(line, index)
        elif line[index] == '*':
            (token, index) = read_star(line, index)
        elif line[index] == '/':
            (token, index) = read_slash(line, index)
        else:
            print('Invalid character found: ' + line[index])
            exit(1)
        tokens.append(token)
    return tokens

# "+", "-"を計算する関数
def evaluate_add_sub(tokens):
    answer = 0
    tokens.insert(0, {'type': 'PLUS'}) # Insert a dummy '+' token
    index = 1
    while index < len(tokens):
        if tokens[index]['type'] == 'NUMBER':
            if tokens[index - 1]['type'] == 'PLUS':
                answer += tokens[index]['number']
            elif tokens[index - 1]['type'] == 'MINUS':
                answer -= tokens[index]['number']
            else:
                print('Invalid syntax')
                exit(1)
        index += 1
    return answer


# "*", "/"を計算する関数
def evaluate_mul_div(tokens):
    new_tokens = [] # '*', '/'を先に計算したtokensを格納
    index = 0
    while index < len(tokens):
        if tokens[index]['type'] == 'NUMBER': # 数字の時、前の演算子が*, /だった時は計算して格納、それ以外は数字のまま格納
            if tokens[index - 1]['type'] == 'STAR':
                left = new_tokens.pop()  # 一つ前の数値を取り出して削除する
                result = left['number'] * tokens[index]['number']
                token = {'type': 'NUMBER', 'number': result}
                new_tokens.append(token)
            elif tokens[index - 1]['type'] == 'SLASH':
                left = new_tokens.pop()  # 一つ前の数値を取り出して削除する
                result = left['number'] / tokens[index]['number']
                token = {'type': 'NUMBER', 'number': result}
                new_tokens.append(token)
            else:
                new_tokens.append(tokens[index])
        elif tokens[index]['type'] in ['PLUS', 'MINUS']: #  演算子(+-)の時は、そのまま格納
            new_tokens.append(tokens[index])
        elif tokens[index]['type'] in ['STAR', 'SLASH']: #  演算子(*/)の時は、格納せずスキップ
            pass
        else:
            print('Invalid syntax')
            exit(1)
        index += 1
    return new_tokens


def test(line):
    tokens = tokenize(line)
    tokens_cal_mul_div = evaluate_mul_div(tokens)
    actual_answer = evaluate_add_sub(tokens_cal_mul_div)
    expected_answer = eval(line)
    if abs(actual_answer - expected_answer) < 1e-8:
        print("PASS! (%s = %f)" % (line, expected_answer))
    else:
        print("FAIL! (%s should be %f but was %f)" % (line, expected_answer, actual_answer))


# Add more tests to this function :)
def run_test():
    print("==== Test started! ====")
    test("1+2")
    test("1.0+2.1-3")
    test("4+3*2-1")
    test("3.5/0.5")
    test("1.5+7.5/3-1.5")

    print("==== Test finished! ====\n")

run_test()

while True:
    print('> ', end="")
    line = input()
    tokens = tokenize(line)
    tokens_cal_mul_div = evaluate_mul_div(tokens)
    answer = evaluate_add_sub(tokens_cal_mul_div)
    print("answer = %f\n" % answer)
