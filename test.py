


if __name__ == '__main__':
    f = open('code_C.txt', 'r', encoding='utf-8')
    contents = f.read()
    chars = set(contents)
    print(chars)