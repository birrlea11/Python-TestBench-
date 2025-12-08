import timeit
import matplotlib.pyplot as plt
import psutil
import threading

ITERATIONS_FLOAT_BENCHMARK = 10000000
NUM_REPEATS_FLOAT = 1
TOTAL_RUNS = 10
SAMPLING_INTERVAL = 0.05


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

    time_taken = run_float_benchmark()

    stop_event.set()
    t1.join()

    return cpuPercent, time_taken


def run_benchmark_and_plot():
    all_cpu_runs = []
    total_time_accumulated = 0

    print(f"Se ruleaza benchmark-ul de {TOTAL_RUNS} ori...")

    for i in range(TOTAL_RUNS):
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
        plt.title('Average CPU Response to Benchmark')
        plt.legend()
        plt.savefig('calculate_pi.png')
        plt.show()
    except Exception:
        pass

    return total_time_accumulated / TOTAL_RUNS


if __name__ == "__main__":
    avg_time = run_benchmark_and_plot()
    print(f"Timp mediu de executie: {avg_time}")