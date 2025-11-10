import multiprocessing

from benchmark_gui import BenchmarkApp
import tkinter as tk

if __name__ == "__main__":
    multiprocessing.freeze_support()

    root = tk.Tk()
    app = BenchmarkApp(root)
    root.mainloop()