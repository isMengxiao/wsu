# -*- coding: utf-8 -*-

def igpay(string):
    vowels = {'a', 'e', 'i', 'o', 'u'}
    if not vowels & set(string):
        return string

    if string[0] in vowels:
        return f"{string}way"

    for i, c in enumerate(string):
        if c not in vowels:
            continue
        return f"{string[i:]}{string[:i]}ay"
    return string

if __name__ == "__main__":
    strings = ["yes", "parrot", "knights", "add", "office", "why"]
    for s in strings:
        print(igpay(s))

