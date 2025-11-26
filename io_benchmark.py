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


def monitor_cpu(stop_event, cpu_data_list):
    psutil.cpu_percent(interval=None)
    while not stop_event.wait(timeout=0.1):
        cpu_usage = psutil.cpu_percent(interval=None)
        cpu_data_list.append(cpu_usage)


def test_write_seq(data_block):
    print(f"Starting write test ({FILE_SIZE_MB} MB)...")
    start_time = time.perf_counter()
    try:
        with open(TEMP_FILE_NAME, 'wb') as f:
            for _ in range(BLOCK_COUNT):
                f.write(data_block)
            f.flush()
            os.fsync(f.fileno())
    except IOError as e:
        print(f"Error: {e}")
        return 0, 0
    end_time = time.perf_counter()
    write_time = end_time - start_time
    write_speed_mbps = FILE_SIZE_MB / write_time
    print(f"Write finished: {write_speed_mbps:.2f} MB/s")
    return write_time, write_speed_mbps


def test_write_rand(data_block):
    print(f"Starting random write test...")
    start_time = time.perf_counter()
    try:
        with open(TEMP_FILE_NAME, 'r+b') as f:
            for i in range(RANDOM_IO_OPERATIONS):
                f.seek(random.randint(0, FILE_SIZE_MB * 1024 * 1024 - RANDOM_IO_BLOCK_SIZE))
                f.write(data_block)
            f.flush()
            os.fsync(f.fileno())
    except IOError as e:
        print(f"Error: {e}")
        return 0, 0
    end_time = time.perf_counter()
    write_time = end_time - start_time
    write_speed_iops = RANDOM_IO_OPERATIONS / write_time
    print(f"Rand Write finished: {write_speed_iops:.2f} op/s")
    return write_time, write_speed_iops


def test_read_seq():
    print(f"Starting read test...")
    start_time = time.perf_counter()
    try:
        with open(TEMP_FILE_NAME, 'rb') as f:
            while f.read(BLOCK_SIZE_BYTES):
                pass
    except IOError as e:
        print(f"Error: {e}")
        return 0, 0
    end_time = time.perf_counter()
    read_time = end_time - start_time
    read_speed_mbps = FILE_SIZE_MB / read_time
    print(f"Read finished: {read_speed_mbps:.2f} MB/s")
    return read_time, read_speed_mbps


def test_read_rand():
    print(f"Starting random read test...")
    start_time = time.perf_counter()
    try:
        with open(TEMP_FILE_NAME, 'rb') as f:
            for i in range(RANDOM_IO_OPERATIONS):
                f.seek(random.randint(0, FILE_SIZE_MB * 1024 * 1024 - RANDOM_IO_BLOCK_SIZE))
                f.read(RANDOM_IO_BLOCK_SIZE)
    except IOError as e:
        print(f"Error: {e}")
        return 0, 0
    end_time = time.perf_counter()
    read_time = end_time - start_time
    read_speed_iops = RANDOM_IO_OPERATIONS / read_time
    print(f"Rand Read finished: {read_speed_iops:.2f} op/s")
    return read_time, read_speed_iops


def cleanup_file():
    try:
        if os.path.exists(TEMP_FILE_NAME):
            os.remove(TEMP_FILE_NAME)
    except OSError:
        pass


def run_io_test():
    cpuPercent = []
    stop_event = threading.Event()

    t1 = threading.Thread(
        target=monitor_cpu,
        args=(stop_event, cpuPercent)
    )
    t1.start()

    print("Generating data block...")
    try:
        data_block = os.urandom(BLOCK_SIZE_BYTES)
        random_data_block = os.urandom(RANDOM_IO_BLOCK_SIZE)
    except MemoryError:
        stop_event.set()
        t1.join()
        return None

    w_time, w_speed = test_write_seq(data_block)
    wr_time, wr_speed = test_write_rand(random_data_block)
    rr_time, rr_speed = test_read_rand()
    r_time, r_speed = test_read_seq()

    cleanup_file()

    stop_event.set()
    t1.join()

    try:
        plt.figure(figsize=(10, 6))
        plt.plot(cpuPercent)
        plt.ylabel('CPU Usage %')
        plt.xlabel('Time (x 0.1 seconds)')
        plt.title('CPU Response during I/O Benchmark')
        plt.savefig('io_benchmark_cpu.png')
        plt.show()
    except Exception:
        pass

    return {
        "write_speed_mbps": w_speed,
        "read_speed_mbps": r_speed,
        "write_speed_rand": wr_speed,
        "read_speed_rand": rr_speed
    }


if __name__ == "__main__":
    run_io_test()