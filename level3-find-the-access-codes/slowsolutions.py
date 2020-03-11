def slowsolutionA(l):
    def lucky(x, y, z):
        return (y % x == 0) and (z % y == 0)
    luckies = 0
    for i in range(len(l)-2):
        for j in range(i+1, len(l)-1):
            for k in range(j+1, len(l)):
                if lucky(l[i], l[j], l[k]):
                    luckies += 1
    return luckies

def slowsolutionB(l):
    luckies = 0
    for i in range(len(l)-2):
        for j in range(i+1, len(l)-1):
            if l[j] % l[i] == 0:
                for k in range(j+1, len(l)):
                    if l[k] % l[j] == 0:
                        luckies += 1
    return luckies
