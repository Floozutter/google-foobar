def solution(s):
    rightwalkers = 0
    salutes = 0
    for c in s:
        if c == ">":
            rightwalkers += 1
        elif c == "<":
            salutes += rightwalkers * 2
    return salutes
