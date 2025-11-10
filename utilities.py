from CiurulLuiEratostene import run_ciurul_lui_Eratostene
from calculPi import run_float_benchmark
from io_benchmark import run_io_test

import random
from itertools import count
import pandas as pd
import matplotlib.pyplot as plt

plt.style.use('fivethirtyeight')
x_vals = []
y_vals = []

LIMIT = 100_000_00
NUM_REPEATS = 10
ITERATIONS_FLOAT_BENCHMARK = 10000000
NUM_REPEATS_FLOAT = 10

def plot_data(x:int,y:int):
    x_vals.append(x)
    y_vals.append(y)

plt.tight_layout()
plt.show()

def run_all_benchmarks():
    """
    Ruleaza toate testele de performanta (Integer, Float si I/O)
    si afiseaza rezultatele.
    """
    try:
        # --- APELUL FUNCTIEI DE BENCHMARK (Operatii cu intregi) ---
        print("\n--- RULARE BENCHMARK CIURUL LUI ERATOSTENE ---")
        time_result = run_ciurul_lui_Eratostene(LIMIT)

        print("\n--- REZULTAT CIURUL LUI ERATOSTENE ---")
        print(f"Limita de cautare (N): {LIMIT:,}")
        print(f"Numar de repetari: {NUM_REPEATS}")
        print(f"Timpul minim de executie (Integer Benchmark): {time_result:.6f} secunde")

        # --- APELUL FUNCTIEI DE BENCHMARK (Operatii cu virgula mobila) ---
        print("\n--- RULARE BENCHMARK CALCUL PI ---")
        time_result_float = run_float_benchmark()

        print("\n--- REZULTAT BENCHMARK CALCUL PI (Floating Point) ---")
        print(f"Iteratii de calcul: {ITERATIONS_FLOAT_BENCHMARK:,}")
        print(f"Timpul minim de executie (Float Benchmark): {time_result_float:.6f} secunde")

        # --- APELUL FUNCTIEI DE BENCHMARK (Operatii I/O Disc) ---
        print("\n--- RULARE BENCHMARK I/O (Disc) ---")
        io_results = run_io_test()

        if io_results:
            print("\n--- REZULTAT BENCHMARK I/O (Disc) ---")
            print("--- Sequential ---")
            print(f"Viteza Scriere: {io_results['write_speed_mbps']:.2f} MB/s")
            print(f"Viteza Citire: {io_results['read_speed_mbps']:.2f} MB/s")

            print("\n--- Random (IOPS) ---")
            # Folosim cheile pe care le-ai definit tu în dicționarul return
            print(f"Citire Aleatorie: {io_results['read_speed_rand']:.2f} op/s")
            print(f"Scriere Aleatorie: {io_results['write_speed_rand']:.2f} op/s")
        else:
            print("\nEroare la rularea benchmark-ului I/O.")


    except Exception as e:
        error_msg = str(e)
        print(f"\nA aparut o eroare neasteptata in timpul benchmark-ului: {e}")

