import timeit
import math

ITERATIONS_FLOAT_BENCHMARK = 1000000
NUM_REPEATS_FLOAT = 10


def run_float_benchmark():


    SETUP_CODE = f"""
def calculate_pi_leibniz(iterations):
    pi = 0.0
    for i in range(iterations):
        term = 1.0 / (2.0 * i + 1.0)
        if i % 2 == 0:
            pi += term
        else:
            pi -= term
    return pi * 4
"""

    TEST_CODE = f"calculate_pi_leibniz({ITERATIONS_FLOAT_BENCHMARK})"

    times = timeit.repeat(
        stmt=TEST_CODE,
        setup=SETUP_CODE,
        repeat=NUM_REPEATS_FLOAT,
        number=1
    )

    return min(times)
