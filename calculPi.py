import timeit
import matplotlib.pyplot as plt
import psutil
import threading

ITERATIONS_FLOAT_BENCHMARK = 2000000
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

def monitor_cpu(stop_event, cpu_data_list):
    psutil.cpu_percent(interval=None)
    while not stop_event.wait(timeout=0.1):
        cpu_usage = psutil.cpu_percent(interval=None)
        cpu_data_list.append(cpu_usage)

def run_benchmark_and_plot():
    cpuPercent = []
    stop_event = threading.Event()

    t1 = threading.Thread(
        target=monitor_cpu,
        args=(stop_event, cpuPercent)
    )
    t1.start()

    result_time = run_float_benchmark()

    stop_event.set()
    t1.join()

    try:
        plt.figure(figsize=(10, 6))
        plt.plot(cpuPercent)
        plt.ylabel('CPU Usage %')
        plt.xlabel('Time (x 0.1 seconds)')
        plt.title('CPU Response to Benchmark')
        plt.savefig('calculate_pi.png')
        plt.show()
    except Exception:
        pass

    return result_time

if __name__ == "__main__":
    print(run_benchmark_and_plot())