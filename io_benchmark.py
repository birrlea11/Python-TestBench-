import os
import time
import random
FILE_SIZE_MB = 256
BLOCK_SIZE_BYTES = 4 * 1024 * 1024
RANDOM_IO_BLOCK_SIZE = 4096
RANDOM_IO_OPERATIONS = 1000
TOTAL_SIZE_BYTES = FILE_SIZE_MB * 1024 * 1024
BLOCK_COUNT = TOTAL_SIZE_BYTES // BLOCK_SIZE_BYTES
TEMP_FILE_NAME = "temp_io_benchmark.tmp"


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
        print(f"Error during write test: {e}")
        return 0, 0

    end_time = time.perf_counter()

    write_time = end_time - start_time
    write_speed_mbps = FILE_SIZE_MB / write_time

    print(f"Write test finished in {write_time:.4f}s ({write_speed_mbps:.2f} MB/s)")
    return write_time, write_speed_mbps

def test_write_rand(data_block):
    print(f"Starting random write test ({FILE_SIZE_MB} MB)...")

    start_time = time.perf_counter()

    try:
        with open(TEMP_FILE_NAME, 'r+b') as f:
            for i in range(RANDOM_IO_OPERATIONS):
                f.seek(random.randint(0, FILE_SIZE_MB*1024*1024 -RANDOM_IO_BLOCK_SIZE))
                f.write(data_block)
            f.flush()
            os.fsync(f.fileno())

    except IOError as e:
        print(f"Error during random write test: {e}")
        return 0, 0

    end_time = time.perf_counter()

    write_time = end_time - start_time
    write_speed_iops = RANDOM_IO_OPERATIONS / write_time

    print(f"Random write test finished in {write_time:.4f}s ({write_speed_iops:.2f} op/s)")
    return write_time, write_speed_iops


def test_read_seq():
    print(f"Starting read test ({FILE_SIZE_MB} MB)...")

    start_time = time.perf_counter()

    try:
        with open(TEMP_FILE_NAME, 'rb') as f:
            while f.read(BLOCK_SIZE_BYTES):
                pass

    except IOError as e:
        print(f"Error during read test: {e}")
        return 0, 0

    end_time = time.perf_counter()

    read_time = end_time - start_time
    read_speed_mbps = FILE_SIZE_MB / read_time

    print(f"Read test finished in {read_time:.4f}s ({read_speed_mbps:.2f} MB/s)")
    return read_time, read_speed_mbps

def test_read_rand():
    print(f"Starting read test ({FILE_SIZE_MB} MB)...")

    start_time = time.perf_counter()

    try:
        with open(TEMP_FILE_NAME, 'rb') as f:
            for i in range(RANDOM_IO_OPERATIONS):
                f.seek(random.randint(0, FILE_SIZE_MB * 1024 * 1024 - RANDOM_IO_BLOCK_SIZE))
                f.read(RANDOM_IO_BLOCK_SIZE)

    except IOError as e:
        print(f"Error during read test: {e}")
        return 0, 0

    end_time = time.perf_counter()

    read_time = end_time - start_time
    read_speed_iops = RANDOM_IO_OPERATIONS / read_time

    print(f"Read rand test finished in {read_time:.4f}s ({read_speed_iops:.2f} op/s)")
    return read_time, read_speed_iops


def cleanup_file():
    try:
        os.remove(TEMP_FILE_NAME)
        print(f"Cleanup: Removed temporary file '{TEMP_FILE_NAME}'.")
    except OSError as e:
        print(f"Error during cleanup: {e}")


def run_io_test():
    print("Generating data block for testing...")
    try:
        data_block = os.urandom(BLOCK_SIZE_BYTES)
        random_data_block = os.urandom(RANDOM_IO_BLOCK_SIZE)
    except MemoryError:
        print(f"Error: Not enough memory to create a {BLOCK_SIZE_BYTES} byte data block.")
        return None

    write_time, write_speed = test_write_seq(data_block)
    write_time_rand, write_speed_rand = test_write_rand(random_data_block)

    read_time_rand, read_speed_rand = test_read_rand()
    read_time, read_speed = test_read_seq()

    cleanup_file()

    return {
        "write_time": write_time,
        "write_speed_mbps": write_speed,
        "read_time": read_time,
        "read_speed_mbps": read_speed,
        "write_time_rand": write_time_rand,
        "write_speed_rand": write_speed_rand,
        "read_time_rand": read_time_rand,
        "read_speed_rand": read_speed_rand
    }


if __name__ == "__main__":
    print("--- Running I/O Benchmark Standalone ---")

    results = run_io_test()

    if results:
        print("\n--- I/O Benchmark Summary ---")
        print(f"File Size: {FILE_SIZE_MB} MB")
        print(f"Write Speed: {results['write_speed_mbps']:.2f} MB/s")
        print(f"Read Speed: {results['read_speed_mbps']:.2f} MB/s")
        print(f"Write Speed Rand: {results['write_speed_rand']:.2f} op/s")
        print(f"Read Speed Rand: {results['read_speed_rand']:.2f} op/s")

