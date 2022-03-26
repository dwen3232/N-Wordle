from collections import Counter

# this is actually reversed; leftmost is least significant value
def base_to_int(s):
    res = 0
    for i, ch in enumerate(s):
        if not 0 <= int(ch) <= 2:
            raise ValueError()
        res += int(ch) * (3 ** i)
    return res



# for changing bases
def int_to_base(s, b):
    BS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    res = ""
    while s:
        res+=BS[s%b]
        s//= b
    return res[::-1] or "0"


# 0 - no match,   1 - contains,   2 - match
def guess(answer, query):
    counter = Counter(answer)
    r = 0
    for i, (a, q) in enumerate(zip(answer, query)):
        t = 0
        if q == a:
            if q in counter:
                counter[q] -= 1
            t = 2
        elif q in counter and counter[q] > 0:
            counter[q] -= 1
            t = 1
        else:
            t = 0
        r += t * (3 ** i)
    return r