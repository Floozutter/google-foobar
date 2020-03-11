from collections import defaultdict

def solution(l):
    # Build dictionary of factor relationships:
    #   - Key: An index to a multiple.
    #   - Value: A set of indices to factors of the multiple.
    factor_indices = defaultdict(set)
    for i in range(len(l)-1):
        for j in range(i+1, len(l)):
            if l[j] % l[i] == 0:
                factor_indices[j].add(i)
    # Count the number of factors of factors, which imply lucky triples.
    luckies = 0
    for m in factor_indices:             # m points to a multiple
        for f in factor_indices[m]:      # f points to a factor of m
            if f in factor_indices:      # check if f is also a multiple
                ffs = factor_indices[f]  # ffs is a set of factors of factors
                luckies += len(ffs)      # add the number of factor factors
    return luckies
