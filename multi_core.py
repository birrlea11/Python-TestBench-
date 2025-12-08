import time
import psutil
import multiprocessing
import threading
import matplotlib.pyplot as plt

ITERATIONS_PER_CORE = 20_000_000
TOTAL_RUNS = 10
SAMPLING_INTERVAL = 0.05


def calculate_pi_leibniz(iterations):
    pi = 0.0
    for i in range(iterations):
        term = 1.0 / (2.0 * i + 1.0)
        if i % 2 == 0:
            pi += term
        else:
            pi -= term
    return pi * 4


def monitor_cpu(stop_event, cpu_data_list):
    psutil.cpu_percent(interval=None)
    while not stop_event.wait(timeout=SAMPLING_INTERVAL):
        cpu_usage = psutil.cpu_percent(interval=None)
        cpu_data_list.append(cpu_usage)


def _execute_single_run():
    cpuPercent = []
    stop_event = threading.Event()

    t1 = threading.Thread(
        target=monitor_cpu,
        args=(stop_event, cpuPercent)
    )
    t1.start()

    core_count = psutil.cpu_count(logical=True)
    iterations_list = [ITERATIONS_PER_CORE] * core_count

    start_time = time.perf_counter()

    with multiprocessing.Pool(processes=core_count) as pool:
        pool.map(calculate_pi_leibniz, iterations_list)

    end_time = time.perf_counter()
    total_time = end_time - start_time

    stop_event.set()
    t1.join()

    return cpuPercent, total_time


def run_multi_core_benchmark():
    all_cpu_runs = []
    total_time_accumulated = 0

    print(f"Se ruleaza Multi-Core Benchmark de {TOTAL_RUNS} ori...")
    print(f"Sarcina per nucleu: {ITERATIONS_PER_CORE:,} iteratii.")

    for i in range(TOTAL_RUNS):
        print(f"Rularea {i + 1}...")
        cpu_data, time_taken = _execute_single_run()
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
        plt.title('Average CPU Response to Multi-Core Benchmark')
        plt.legend()
        plt.savefig('multicore_benchmark.png')
        plt.show()
    except Exception:
        pass

    return total_time_accumulated / TOTAL_RUNS


if __name__ == "__main__":
    multiprocessing.freeze_support()
    avg_time = run_multi_core_benchmark()
    print("-" * 30)
    print(f"Timp mediu de executie (toate nucleele): {avg_time:.6f} secunde")