import timeit
import matplotlib.pyplot as plt
import psutil
import threading

LIMIT = 10_000_000
NUM_REPEATS = 10

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
    while not stop_event.wait(timeout=0.1):
        cpu_usage = psutil.cpu_percent(interval=None)
        cpu_data_list.append(cpu_usage)

def run_ciur_and_plot(limit=LIMIT):
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

    try:
        plt.figure(figsize=(10, 6))
        plt.plot(cpuPercent)
        plt.ylabel('CPU Usage %')
        plt.xlabel('Time (x 0.1 seconds)')
        plt.title('CPU Response to Ciur Benchmark')
        plt.savefig('ciur_benchmark.png')
        plt.show()
    except Exception:
        pass

    return result_time

if __name__ == "__main__":
    print(run_ciur_and_plot())