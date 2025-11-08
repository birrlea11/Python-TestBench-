import time
import psutil
import multiprocessing

ITERATIONS_PER_CORE = 2_000_000


def calculate_pi_leibniz(iterations):
    pi = 0.0
    for i in range(iterations):
        term = 1.0 / (2.0 * i + 1.0)
        if i % 2 == 0:
            pi += term
        else:
            pi -= term
    return pi * 4


def run_multi_core_benchmark():
    print("Pornire test de stres Multi-Core (Multiprocessing)...")

    try:
        core_count = psutil.cpu_count(logical=True)
        print(f"S-au detectat {core_count} nuclee logice.")
        print(f"Se pornesc {core_count} procese, fiecare va calcula Pi cu {ITERATIONS_PER_CORE:,} iterații.")

        iterations_list = [ITERATIONS_PER_CORE] * core_count

        start_time = time.perf_counter()

        with multiprocessing.Pool(processes=core_count) as pool:
            pool.map(calculate_pi_leibniz, iterations_list)

        end_time = time.perf_counter()

        total_time = end_time - start_time

        print("\n" + "=" * 30)
        print("--- Rezultat Test Multi-Core ---")
        print(f"Timp total pentru {core_count} nuclee: {total_time:.6f} secunde")
        print("=" * 30)

    except Exception as e:
        print(f"A apărut o eroare în timpul testului multi-core: {e}")


if __name__ == "__main__":
    multiprocessing.freeze_support()
    run_multi_core_benchmark()