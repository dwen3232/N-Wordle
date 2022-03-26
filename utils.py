from collections import Counter


# this is actually reversed; leftmost is least significant value
def base_to_int(s, b):
    res = 0
    for i, ch in enumerate(s):
        if not 0 <= int(ch) <= 2:
            raise ValueError()
        res += int(ch) * (b ** i)
    return res


# for changing bases
def int_to_base(s, b):
    BS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    res = ""
    while s:
        res += BS[s % b]
        s //= b
    return res[::-1] or "0"


# 0 - no match,   1 - contains,   2 - match
def guess(answer, query):
    counter = Counter(answer)
    r = 0
    for i, (a, q) in enumerate(zip(answer, query)):
        t = 0
        if q == a:
            counter[q] -= 1
            # if q in counter:
            #     counter[q] -= 1
            t = 2
        elif q in counter and counter[q] > 0:
            counter[q] -= 1
            t = 1
        else:
            t = 0
        r += t * (3 ** i)
    return r


def is_guess_valid(answer, query, guess_code):
    counter = Counter(answer)
    for q, w in zip(query, answer):
        r = guess_code % 3
        if r == 0 and q in answer:
            return False
        elif r == 1 and (q == w or (q in counter and counter[q] == 0)):
            return False
        elif r == 2 and q != w:
            return False
        # decrement counter
        if q in counter:
            counter[q] -= 1
    return True
