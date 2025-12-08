import os
import time
import random
import psutil
import threading
import matplotlib.pyplot as plt

FILE_SIZE_MB = 256
BLOCK_SIZE_BYTES = 4 * 1024 * 1024
RANDOM_IO_BLOCK_SIZE = 4096
RANDOM_IO_OPERATIONS = 1000
TOTAL_SIZE_BYTES = FILE_SIZE_MB * 1024 * 1024
BLOCK_COUNT = TOTAL_SIZE_BYTES // BLOCK_SIZE_BYTES
TEMP_FILE_NAME = "temp_io_benchmark.tmp"

TOTAL_RUNS = 10
SAMPLING_INTERVAL = 0.05


def monitor_cpu(stop_event, cpu_data_list):
    psutil.cpu_percent(interval=None)
    while not stop_event.wait(timeout=SAMPLING_INTERVAL):
        cpu_usage = psutil.cpu_percent(interval=None)
        cpu_data_list.append(cpu_usage)


def test_write_seq(data_block):
    start_time = time.perf_counter()
    try:
        with open(TEMP_FILE_NAME, 'wb') as f:
            for _ in range(BLOCK_COUNT):
                f.write(data_block)
            f.flush()
            os.fsync(f.fileno())
    except IOError:
        return 0, 0
    end_time = time.perf_counter()
    write_time = end_time - start_time
    write_speed_mbps = FILE_SIZE_MB / write_time if write_time > 0 else 0
    return write_time, write_speed_mbps


def test_write_rand(data_block):
    start_time = time.perf_counter()
    try:
        with open(TEMP_FILE_NAME, 'r+b') as f:
            for i in range(RANDOM_IO_OPERATIONS):
                f.seek(random.randint(0, FILE_SIZE_MB * 1024 * 1024 - RANDOM_IO_BLOCK_SIZE))
                f.write(data_block)
            f.flush()
            os.fsync(f.fileno())
    except IOError:
        return 0, 0
    end_time = time.perf_counter()
    write_time = end_time - start_time
    write_speed_iops = RANDOM_IO_OPERATIONS / write_time if write_time > 0 else 0
    return write_time, write_speed_iops


def test_read_seq():
    start_time = time.perf_counter()
    try:
        with open(TEMP_FILE_NAME, 'rb') as f:
            while f.read(BLOCK_SIZE_BYTES):
                pass
    except IOError:
        return 0, 0
    end_time = time.perf_counter()
    read_time = end_time - start_time
    read_speed_mbps = FILE_SIZE_MB / read_time if read_time > 0 else 0
    return read_time, read_speed_mbps


def test_read_rand():
    start_time = time.perf_counter()
    try:
        with open(TEMP_FILE_NAME, 'rb') as f:
            for i in range(RANDOM_IO_OPERATIONS):
                f.seek(random.randint(0, FILE_SIZE_MB * 1024 * 1024 - RANDOM_IO_BLOCK_SIZE))
                f.read(RANDOM_IO_BLOCK_SIZE)
    except IOError:
        return 0, 0
    end_time = time.perf_counter()
    read_time = end_time - start_time
    read_speed_iops = RANDOM_IO_OPERATIONS / read_time if read_time > 0 else 0
    return read_time, read_speed_iops


def cleanup_file():
    try:
        if os.path.exists(TEMP_FILE_NAME):
            os.remove(TEMP_FILE_NAME)
    except OSError:
        pass


def _execute_single_run():
    cpuPercent = []
    stop_event = threading.Event()

    try:
        data_block = os.urandom(BLOCK_SIZE_BYTES)
        random_data_block = os.urandom(RANDOM_IO_BLOCK_SIZE)
    except MemoryError:
        return [], {}

    t1 = threading.Thread(
        target=monitor_cpu,
        args=(stop_event, cpuPercent)
    )
    t1.start()

    w_time, w_speed = test_write_seq(data_block)
    wr_time, wr_speed = test_write_rand(random_data_block)
    rr_time, rr_speed = test_read_rand()
    r_time, r_speed = test_read_seq()

    cleanup_file()

    stop_event.set()
    t1.join()

    metrics = {
        "write_speed_mbps": w_speed,
        "read_speed_mbps": r_speed,
        "write_speed_rand": wr_speed,
        "read_speed_rand": rr_speed
    }

    return cpuPercent, metrics


def run_io_test():
    all_cpu_runs = []
    accumulated_metrics = {
        "write_speed_mbps": 0,
        "read_speed_mbps": 0,
        "write_speed_rand": 0,
        "read_speed_rand": 0
    }

    print(f"Se ruleaza IO Benchmark de {TOTAL_RUNS} ori...")

    for i in range(TOTAL_RUNS):
        print(f"Rularea {i + 1}...")
        cpu_data, metrics = _execute_single_run()

        if cpu_data:
            all_cpu_runs.append(cpu_data)
            for key in accumulated_metrics:
                accumulated_metrics[key] += metrics[key]

    if not all_cpu_runs:
        return {}

    min_length = min(len(run) for run in all_cpu_runs)
    average_cpu = []
    for i in range(min_length):
        total_val = sum(run[i] for run in all_cpu_runs)
        average_cpu.append(total_val / len(all_cpu_runs))

    averaged_results = {k: v / len(all_cpu_runs) for k, v in accumulated_metrics.items()}

    try:
        plt.figure(figsize=(10, 6))
        plt.plot(average_cpu, label=f'Average CPU Usage ({TOTAL_RUNS} runs)')
        plt.ylabel('CPU Usage %')
        plt.xlabel(f'Time (x {SAMPLING_INTERVAL} seconds)')
        plt.title('Average CPU Response during I/O Benchmark')
        plt.legend()
        plt.savefig('io_benchmark_cpu.png')
        plt.show()
    except Exception:
        pass

    return averaged_results


if __name__ == "__main__":
    results = run_io_test()
    print("-" * 30)
    print("REZULTATE MEDII:")
    print(f"Seq Write: {results.get('write_speed_mbps', 0):.2f} MB/s")
    print(f"Rand Write: {results.get('write_speed_rand', 0):.2f} ops/s")
    print(f"Rand Read:  {results.get('read_speed_rand', 0):.2f} ops/s")
    print(f"Seq Read:  {results.get('read_speed_mbps', 0):.2f} MB/s")