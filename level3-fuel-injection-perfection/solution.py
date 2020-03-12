from itertools import takewhile

def halvability(n):
    """Returns the number of times n can be evenly halved."""
    binstr = bin(n)[::-1]  # Get reversed binary string.
    # Count the number of consecutive zeroes.
    return sum(1 for _ in takewhile(lambda bit: bit=="0", binstr))

def solution(n):
    n = int(n)  # Convert from string to integer.
    ops = 0
    while n != 1:  # Done when one.
        # Divide by two whenever possible.
        half, remainder = divmod(n, 2)
        if remainder == 0:
            n = half
            ops += 1
        # Surprisingly, 3 is an edge case for the following.
        elif n == 3:
            n = 1
            ops += 2
        # Decide whether to increment or decrement by halvability.
        elif halvability(n+1) > halvability(n-1):
            n = n + 1
            ops += 1
        else:
            n = n - 1
            ops += 1
    return ops
