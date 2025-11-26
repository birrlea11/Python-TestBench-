import os
import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
import sys
import io
from os import walk
import psutil

from utilities import run_all_benchmarks
from PIL import Image
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib import pyplot as plt
from matplotlib import image as mpimg
from hardware_info import display_hardware_info
from CiurulLuiEratostene import run_ciurul_lui_Eratostene, LIMIT, run_ciur_and_plot
from calculPi import run_float_benchmark, ITERATIONS_FLOAT_BENCHMARK, run_benchmark_and_plot
from io_benchmark import run_io_test
from multi_core import run_multi_core_benchmark



class TextRedirector(io.TextIOBase):
    def __init__(self, widget):
        self.widget = widget

    def write(self, s):
        self.widget.after(0, self.update_text, s)

    def update_text(self, s):
        try:
            self.widget.configure(state='normal')
            self.widget.insert(tk.END, s)
            self.widget.see(tk.END)
            self.widget.configure(state='disabled')
        except tk.TclError:
            pass


def open_png(file_name):
    image = Image.open(file_name)
    image.show()


class BenchmarkApp:
    def __init__(self, root):
        self.root = root
        root.title("Benchmark & System Info GUI")
        root.geometry("800x600")

        self.buttons = []
        self.live_data_running = False
        self.live_data_label = None
        self.live_data_window = None
        self.cpu_data = []
        self.ram_data = []
        top_frame = ttk.Frame(root, padding="10")
        top_frame.pack(fill='x', side='top')

        button_frame = ttk.Labelframe(top_frame, text="Tests", padding="10")
        button_frame.pack(side='left', fill='y', padx=(0, 10))

        live_button_frame = ttk.Labelframe(top_frame, text="Monitoring", padding="10")
        live_button_frame.pack(side='left', fill='y', padx=10)

        output_frame = ttk.Labelframe(root, text="Output Console", padding="10")
        output_frame.pack(fill='both', expand=True, side='bottom', padx=10, pady=(0, 10))

        self.add_button(button_frame, "Get Hardware Info", self.run_hw_info)
        self.add_button(button_frame, "Test: Single-Core Integer", self.run_integer_test)
        self.add_button(button_frame, "Test: Single-Core Float", self.run_float_test)
        self.add_button(button_frame, "Test: Multi-Core (Stress CPU)", self.run_multi_core_test)
        self.add_button(button_frame, "Test: I/O Ops (Disk)", self.run_io_test)
        self.add_button(button_frame, "Run FULL Testbench", self.run_all_tests)

        live_button = ttk.Button(live_button_frame, text="Show Live Data", command=self.open_live_data_window)
        live_button.pack(pady=5, anchor='n')
        self.buttons.append(live_button)


        project_root = os.path.dirname(os.path.abspath(__file__))

        try:
            for root_dir, dirs, files in os.walk(project_root):
                if '.venv' in root_dir or '__pycache__' in root_dir or '.git' in root_dir:
                    continue

                for file in files:
                    if file.endswith('.png'):
                        btn_text = f"Open {file}"
                        b = ttk.Button(live_button_frame, text=btn_text, command=lambda f=file: open_png(f))
                        b.pack(pady=2, anchor='n')
                        self.buttons.append(b)
        except Exception as e:
            print(f"Warning: Could not scan files: {e}")


        self.output_text = ScrolledText(output_frame, state='disabled', height=10, bg="#2b2b2b", fg="#f0f0f0",
                                        font=("Consolas", 10))
        self.output_text.pack(fill='both', expand=True)

        self.redirector = TextRedirector(self.output_text)
        sys.stdout = self.redirector
        sys.stderr = self.redirector

        print("Application Ready. Select a test to begin.")

        root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def add_button(self, parent, text, command):
        button = ttk.Button(parent, text=text, command=command)
        button.pack(fill='x', pady=5)
        self.buttons.append(button)

    def set_buttons_state(self, state):
        for button in self.buttons:
            try:
                button.configure(state=state)
            except tk.TclError:
                pass

    def clear_output(self):
        self.output_text.configure(state='normal')
        self.output_text.delete('1.0', tk.END)
        self.output_text.configure(state='disabled')

    def center_window(self, window_to_center):
        window_to_center.update_idletasks()

        self.root.update_idletasks()
        root_x = self.root.winfo_x()
        root_y = self.root.winfo_y()
        root_w = self.root.winfo_width()
        root_h = self.root.winfo_height()

        win_w = window_to_center.winfo_width()
        win_h = window_to_center.winfo_height()

        x = root_x + (root_w - win_w) // 2
        y = root_y + (root_h - win_h) // 2

        window_to_center.geometry(f"+{x}+{y}")

    def create_popup(self, message):
        popup = tk.Toplevel(self.root)
        popup.title("Test in Progress")

        tk.Label(popup, text=message, font=("Arial", 12), padx=20, pady=20).pack()

        popup.transient(self.root)
        popup.grab_set()
        popup.resizable(False, False)

        self.center_window(popup)

        return popup

    def run_test_blocking(self, target_function, *args):
        self.set_buttons_state('disabled')
        popup = self.create_popup("Running test... Please wait.\nThe GUI will be unresponsive.")

        self.root.update()

        self.clear_output()
        print(f"Starting test: {target_function.__name__}...\n" + "=" * 30 + "\n")

        try:
            target_function(*args)
            print("\n" + "=" * 30 + f"\n...Test {target_function.__name__} finished.")
        except Exception as e:
            print(f"An exception occurred: {e}")
        finally:
            popup.destroy()
            self.set_buttons_state('normal')

    def run_hw_info(self):
        self.run_test_blocking(display_hardware_info)

    def run_integer_test(self):
        def int_test_target():
            result = run_ciur_and_plot(LIMIT)
            print(f"\n--- Rezultat Ciurul lui Eratostene ---")
            print(f"Timpul minim: {result:.6f} secunde")

        self.run_test_blocking(int_test_target)

    def run_float_test(self):
        def float_test_target():
            # Call the new function that handles the plot internally
            result = run_benchmark_and_plot()

            print(f"\n--- Rezultat Calcul Pi ---")
            print(f"Timpul minim: {result:.6f} secunde")
            print("Graficul a fost salvat (calculate_pi.png) si afisat.")

        self.run_test_blocking(float_test_target)

    def run_multi_core_test(self):
        self.run_test_blocking(run_multi_core_benchmark)

    def run_io_test(self):
        self.run_test_blocking(run_io_test)

    def run_all_tests(self):
        self.run_test_blocking(run_all_benchmarks)

    def open_live_data_window(self):
        if self.live_data_window is not None:
            try:
                self.live_data_window.lift()
                return
            except tk.TclError:
                self.live_data_window = None

        self.live_data_window = tk.Toplevel(self.root)
        self.live_data_window.title("Live System Data Plot")
        self.live_data_window.geometry("600x500")


        self.live_data_figure = Figure(figsize=(6, 4), dpi=100)
        self.live_data_plot = self.live_data_figure.add_subplot(111)

        self.live_data_canvas = FigureCanvasTkAgg(self.live_data_figure, master=self.live_data_window)

        toolbar = NavigationToolbar2Tk(self.live_data_canvas, self.live_data_window)
        toolbar.update()

        self.live_data_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)


        self.center_window(self.live_data_window)
        self.live_data_running = True
        self.cpu_data.clear()
        self.ram_data.clear()
        self.update_live_data_plot()

        self.live_data_window.protocol("WM_DELETE_WINDOW", self.on_closing_live_window)

    def on_closing_live_window(self):
        self.live_data_running = False
        if self.live_data_window:
            self.live_data_window.destroy()
        self.live_data_window = None

    def update_live_data_plot(self):
        try:
            if not self.live_data_running:
                return
            cpu = psutil.cpu_percent()
            ram = psutil.virtual_memory().percent
            self.cpu_data.append(cpu)
            self.ram_data.append(ram)

            if len(self.cpu_data) > 50:
                self.cpu_data.pop(0)
            if len(self.ram_data) > 50:
                self.ram_data.pop(0)

            self.live_data_plot.clear()

            self.live_data_plot.plot(self.cpu_data, label='CPU %')
            self.live_data_plot.plot(self.ram_data, label='RAM %')

            self.live_data_plot.set_title("Live CPU and RAM Usage")
            self.live_data_plot.set_ylabel("Usage (%)")
            self.live_data_plot.set_ylim(0, 100)
            self.live_data_plot.set_xlabel("Time")

            self.live_data_plot.legend()

            self.live_data_canvas.draw()

            self.root.after(1000, self.update_live_data_plot)

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
        except tk.TclError:
            self.live_data_running = False
            self.live_data_window = None

    def on_closing(self):
        print("\nShutting down...")
        self.live_data_running = False
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__
        self.root.destroy()


