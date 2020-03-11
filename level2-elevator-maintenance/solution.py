from functools import cmp_to_key

def version_compare(verstrA, verstrB):
    numsA = [int(s) for s in verstrA.split(".")]
    numsB = [int(s) for s in verstrB.split(".")]
    for a, b in zip(numsA, numsB):
        if a > b:
            return 1
        elif a < b:
            return -1
    if len(numsA) > len(numsB):
        return 1
    elif len(numsA) < len(numsB):
        return -1
    return 0

def solution(l):
    return sorted(l, key=cmp_to_key(version_compare))
