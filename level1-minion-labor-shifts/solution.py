from collections import Counter

def solution(data, n):
    counts = Counter(data)
    return list(filter(lambda z: counts[z] <= n, data))
