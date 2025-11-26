import threading
import psutil
import matplotlib.pyplot as plt
import time

from CiurulLuiEratostene import run_ciurul_lui_Eratostene, run_ciur_and_plot
from calculPi import run_float_benchmark, run_benchmark_and_plot
from io_benchmark import run_io_test
from multi_core import run_multi_core_benchmark

LIMIT = 10_000_000
NUM_REPEATS = 10
ITERATIONS_FLOAT_BENCHMARK = 10000000
NUM_REPEATS_FLOAT = 10


def monitor_cpu(stop_event, cpu_data_list):
    psutil.cpu_percent(interval=None)
    while not stop_event.wait(timeout=0.1):
        cpu_usage = psutil.cpu_percent(interval=None)
        cpu_data_list.append(cpu_usage)


def run_all_benchmarks():
    #referinta laptopul meu
    REF_TIME_INT = 0.830944
    REF_TIME_FLOAT = 0.310641
    REF_TIME_MULTI = 4.759809

    REF_IO_SEQ_WRITE = 94.34
    REF_IO_SEQ_READ = 2422.12
    REF_IO_RAND_WRITE = 1157.31
    REF_IO_RAND_READ = 68875.74

    MAX_SCORE_CPU = 250
    MAX_SCORE_FLOAT = 250
    MAX_SCORE_MULTI = 250
    MAX_SCORE_IO = 250

    cpu_data = []
    stop_event = threading.Event()
    monitor_thread = threading.Thread(target=monitor_cpu, args=(stop_event, cpu_data))

    try:
        print("\n\n")
        print("=" * 60)
        print(f"{'BENCHMARK':^60}")
        print("=" * 60)

        monitor_thread.start()

        # ciur
        print("\n" + "-" * 60)
        print(f"{'[ 1 / 4 ] Integer ALU Test (Single-Core)':^60}")
        print("-" * 60)

        time_int = run_ciur_and_plot(LIMIT)
        score_int = (REF_TIME_INT / time_int) * MAX_SCORE_CPU if time_int > 0 else 0
        print(f"\n>>> Time: {time_int:.4f} s")

        # -calcul pi
        print("\n" + "-" * 60)
        print(f"{'[ 2 / 4 ] Floating Point Test (Single-Core)':^60}")
        print("-" * 60)

        time_float = run_benchmark_and_plot()
        score_float = (REF_TIME_FLOAT / time_float) * MAX_SCORE_FLOAT if time_float > 0 else 0
        print(f"\n>>> Time: {time_float:.4f} s")

        # IO
        print("\n" + "-" * 60)
        print(f"{'[ 3 / 4 ] Disk I/O Performance':^60}")
        print("-" * 60)

        io_res = run_io_test()

        score_io_total = 0
        if io_res:
            part_score = MAX_SCORE_IO / 4
            s_seq_w = (io_res['write_speed_mbps'] / REF_IO_SEQ_WRITE) * part_score
            s_seq_r = (io_res['read_speed_mbps'] / REF_IO_SEQ_READ) * part_score
            s_rnd_w = (io_res['write_speed_rand'] / REF_IO_RAND_WRITE) * part_score
            s_rnd_r = (io_res['read_speed_rand'] / REF_IO_RAND_READ) * part_score
            score_io_total = s_seq_w + s_seq_r + s_rnd_w + s_rnd_r

            # io test afisare
            print("\n>>> Disk Summary:")
            print(f"    Seq Write: {io_res['write_speed_mbps']:>10.2f} MB/s")
            print(f"    Seq Read:  {io_res['read_speed_mbps']:>10.2f} MB/s")
            print(f"    Rnd Write: {io_res['write_speed_rand']:>10.2f} IOPS")
            print(f"    Rnd Read:  {io_res['read_speed_rand']:>10.2f} IOPS")
        else:
            print("I/O Error")

        # 4 multi core
        print("\n" + "-" * 60)
        print(f"{'[ 4 / 4 ] Multi-Core Stress Test':^60}")
        print("-" * 60)

        time_multi = run_multi_core_benchmark()
        score_multi = (REF_TIME_MULTI / time_multi) * MAX_SCORE_MULTI if time_multi > 0 else 0

        stop_event.set()
        monitor_thread.join()

        total_score = int(score_int + score_float + score_io_total + score_multi)
        #tabel final
        print("\n\n")
        print("=" * 60)
        print(f"{'FINAL PERFORMANCE REPORT':^60}")
        print("=" * 60)
        print(f"{'TEST NAME':<30} {'RESULT':<15} {'SCORE':>10}")
        print("-" * 60)
        print(f"{'Integer (Single-Core)':<30} {time_int:<10.4f} s   {int(score_int):>10}")
        print(f"{'Float (Single-Core)':<30} {time_float:<10.4f} s   {int(score_float):>10}")
        print(f"{'Disk I/O (Mixed)':<30} {'See Above':<10}     {int(score_io_total):>10}")
        print(f"{'Multi-Core':<30} {time_multi:<10.4f} s   {int(score_multi):>10}")
        print("=" * 60)
        print(f"{'TOTAL SYSTEM SCORE':<45} {total_score:>12}")
        print("=" * 60)
        print("\n")

        try:
            plt.figure(figsize=(10, 6))
            plt.plot(cpu_data, label='CPU Usage %', color='blue')
            plt.ylabel('CPU Usage %')
            plt.xlabel('Time')
            plt.title('FULL Benchmark-Test CPU Monitor')
            plt.legend()
            plt.savefig('full_benchmark.png')
            plt.show()
        except Exception:
            pass

    except Exception as e:
        print(f"\nError: {e}")
        stop_event.set()


if __name__ == "__main__":
    run_all_benchmarks()