from collections import defaultdict

def solution(l):
    # Build dictionary of factor relationships:
    #   - Key: An index to a multiple.
    #   - Value: A set of indices to factors of the multiple.
    mult2fact = defaultdict(set)
    for i in range(len(l)-1):
        for j in range(i+1, len(l)):
            if l[j] % l[i] == 0:
                mult2fact[j].add(i)
    # Count the number of factors of factors, which imply lucky triples.
    luckies = 0
    for m in mult2fact:              # m is a multiple
        for f in mult2fact[m]:       # f is a factor of m
            if f in mult2fact:       # check if f is also a multiple
                ffs = mult2fact[f]   # ffs is the set of factors of f
                luckies += len(ffs)  # increment the number of factor factors
    return luckies
