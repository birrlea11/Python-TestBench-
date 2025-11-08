import timeit
import math

LIMIT = 100_000_00
NUM_REPEATS = 10


def run_ciurul_lui_Eratostene(limit):


    SETUP_CODE = f"""
def ciurul_lui_Eratostene(n):
    # Initializam lista booleana. True inseamna "potential prim".
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False

    p = 2
    while p * p <= n:
        if is_prime[p]:
            for i in range(p * p, n + 1, p):
                is_prime[i] = False
        p += 1

    return is_prime
"""

    TEST_CODE = f"ciurul_lui_Eratostene({limit})"

    # timeit.repeat ruleaza codul de test de N ori.
    times = timeit.repeat(
        stmt=TEST_CODE,
        setup=SETUP_CODE,
        repeat=NUM_REPEATS,
        number=1
    )

    return min(times)


