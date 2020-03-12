def solutionNaive(n):
    # Done when one.
    if n == 1:
        return 0
    # Divide by two whenever possible.
    half, remainder = divmod(n, 2)
    if remainder == 0:
        return 1 + solutionNaive(half)
    # Decide whether to increment or decrement.
    return min(
        1 + solutionNaive(n-1),
        1 + solutionNaive(n+1)
    )

def solutionA(n):
    def pow2_ceil(n):
        """Returns the closest power of two greater than n."""
        return 2**n.bit_length()
    # Done when one.
    if n == 1:
        return 0
    # Divide by two whenever possible.
    half, remainder = divmod(n, 2)
    if remainder == 0:
        return 1 + solutionA(half)
    # Decide whether to increment or decrement.
    upper = pow2_ceil(n)
    lower = upper // 2
    if upper - n < n - lower:  # Go towards the closer power of two.
        return 1 + solutionA(n+1)
    else:
        return 1 + solutionA(n-1)

from itertools import takewhile
def solutionB(n):
    def halvability(n):
        """Returns the number of times n can be evenly halved."""
        binstr = bin(n)[::-1]  # Get reversed binary string.
        # Count the number of consecutive zeroes.
        return sum(1 for _ in takewhile(lambda bit: bit=="0", binstr))
    # Done when one.
    if n == 1:
        return 0
    # Divide by two whenever possible.
    half, remainder = divmod(n, 2)
    if remainder == 0:
        return 1 + solutionB(half)
    # Surprisingly, 3 is an edge case for the following.
    if n == 3:
        return 2
    # Decide whether to increment or decrement.
    if halvability(n+1) > halvability(n-1):  # Go towards consecutive halves.
        return 1 + solutionB(n+1)
    else:
        return 1 + solutionB(n-1)
    

for i in range(1, 1001):
    target = solutionNaive(i)
    tested = solutionB(i)
    print(f"{i: >4}: {target: >2}, {tested: >2}", end="  | ")
    print("SAME" if target==tested else "DIFF") 
