import timeit
import matplotlib.pyplot as plt
import psutil
import threading

LIMIT = 15_000_000
NUM_REPEATS = 1
TOTAL_RUNS = 10
SAMPLING_INTERVAL = 0.05


def run_ciurul_lui_Eratostene(limit):
    SETUP_CODE = f"""
def ciurul_lui_Eratostene(n):
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

    times = timeit.repeat(
        stmt=TEST_CODE,
        setup=SETUP_CODE,
        repeat=NUM_REPEATS,
        number=1
    )

    return min(times)


def monitor_cpu(stop_event, cpu_data_list):
    psutil.cpu_percent(interval=None)
    while not stop_event.wait(timeout=SAMPLING_INTERVAL):
        cpu_usage = psutil.cpu_percent(interval=None)
        cpu_data_list.append(cpu_usage)


def _execute_single_run(limit):
    cpuPercent = []
    stop_event = threading.Event()

    t1 = threading.Thread(
        target=monitor_cpu,
        args=(stop_event, cpuPercent)
    )
    t1.start()

    result_time = run_ciurul_lui_Eratostene(limit)

    stop_event.set()
    t1.join()

    return cpuPercent, result_time


def run_ciur_and_plot(limit=LIMIT):
    all_cpu_runs = []
    total_time_accumulated = 0

    print(f"Se ruleaza Ciurul lui Eratostene de {TOTAL_RUNS} ori...")

    for i in range(TOTAL_RUNS):
        cpu_data, time_taken = _execute_single_run(limit)
        all_cpu_runs.append(cpu_data)
        total_time_accumulated += time_taken

    if not all_cpu_runs:
        return 0

    min_length = min(len(run) for run in all_cpu_runs)

    average_cpu = []
    for i in range(min_length):
        total_val = sum(run[i] for run in all_cpu_runs)
        average_cpu.append(total_val / TOTAL_RUNS)

    try:
        plt.figure(figsize=(10, 6))
        plt.plot(average_cpu, label=f'Average CPU Usage ({TOTAL_RUNS} runs)')
        plt.ylabel('CPU Usage %')
        plt.xlabel(f'Time (x {SAMPLING_INTERVAL} seconds)')
        plt.title('Average CPU Response to Ciur Benchmark')
        plt.legend()
        plt.savefig('ciur_benchmark.png')
        plt.show()
    except Exception:
        pass

    return total_time_accumulated / TOTAL_RUNS


if __name__ == "__main__":
    avg_time = run_ciur_and_plot()
    print(f"Timp mediu de executie: {avg_time}")