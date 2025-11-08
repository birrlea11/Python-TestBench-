import cpuinfo
import psutil
import os

# --- Functii Ajutatoare pentru Conversie ---

def bytes_to_gigabytes(bytes_val):
    return round(bytes_val / (1024 ** 3), 2)


def bytes_to_megabytes(bytes_val):
    return round(bytes_val / (1024 ** 2), 2)


# --- Functia Principala de Colectare ---

def display_hardware_info():
    """
    Colecteaza si afiseaza informatiile detaliate despre
    CPU, Memorie, Stocare si Retea.
    """
    print("Se colecteaza informatiile despre sistem. Va rugam asteptati...")

    try:
        info = cpuinfo.get_cpu_info()
        logical_cores = psutil.cpu_count(logical=True)
        physical_cores = psutil.cpu_count(logical=False)

        if not info:
            print("\nEroare: Nu s-au putut colecta detaliile despre procesor.")
            return

        print("\n--- DETALII PROCESOR (CPUID) ---")

        print(f"Numele complet de Brand (brand_raw): {info.get('brand_raw', 'N/A')}")
        print(f"Frecventa declarata (GHz): {info.get('hz_advertised_friendly', 'N/A')}")
        print(f"Vendor ID: {info.get('vendor_id_raw', 'N/A')}")
        print(f"Nuclee Fizice: {physical_cores}")
        print(f"Nuclee Logice: {logical_cores}")
        print(f"L2 Cache: {info.get('l2_cache_size', 'N/A')}")
        print(
            f"Family/Model/Stepping: {info.get('family', 'N/A')}/{info.get('model', 'N/A')}/{info.get('stepping', 'N/A')}")

        mem = psutil.virtual_memory()
        swap = psutil.swap_memory()

        print("\n--- DETALII MEMORIE (RAM) ---")
        print(f"Total RAM: {bytes_to_gigabytes(mem.total)} GB")
        print(f"RAM Disponibila: {bytes_to_gigabytes(mem.available)} GB")
        print(f"RAM Utilizata: {bytes_to_gigabytes(mem.used)} GB ({mem.percent}%)")

        if swap.total > 0:
            print(f"\n--- DETALII MEMORIE SWAP ---")
            print(f"Total SWAP: {bytes_to_gigabytes(swap.total)} GB")
            print(f"SWAP Utilizat: {bytes_to_gigabytes(swap.used)} GB ({swap.percent}%)")
            print(
                f"Date SWAP in/out (in/out): {bytes_to_megabytes(swap.sin)} MB / {bytes_to_megabytes(swap.sout)} MB")

        partitions = psutil.disk_partitions(all=False)
        print("\n--- DETALII STOCARE (Discuri Fizice) ---")

        if not partitions:
            print("Nu au fost detectate partitii montate.")

        for partition in partitions:
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                print(f"\n  Dispozitiv: {partition.device}")
                print(f"    Punct de montare: {partition.mountpoint}")
                print(f"    Tip Fs: {partition.fstype}")
                print(f"    Total: {bytes_to_gigabytes(usage.total)} GB")
                print(f"    Utilizat: {bytes_to_gigabytes(usage.used)} GB ({usage.percent}%)")
                print(f"    Liber: {bytes_to_gigabytes(usage.free)} GB")
            except PermissionError:
                print(f"  Eroare de Permisiune pentru partitia: {partition.device}")
            except Exception as e:
                print(f"  Eroare la citirea partitiei {partition.device}: {e}")

        net_io = psutil.net_io_counters()

        print("\n--- DETALII PLACA DE RETEA (Trafic Total) ---")
        print(f"Bytes Trimisi: {bytes_to_megabytes(net_io.bytes_sent)} MB")
        print(f"Bytes Primiti: {bytes_to_megabytes(net_io.bytes_recv)} MB")
        print(f"Pachete Trimise: {net_io.packets_sent}")
        print(f"Pachete Primite: {net_io.packets_recv}")

    except Exception as e:
        print(f"\nA aparut o eroare neasteptata la colectarea datelor: {e}")


# Acest if __name__ == "__main__" iti permite sa rulezi acest fisier
# de sine statator pentru a-l testa, daca doresti.
if __name__ == "__main__":
    display_hardware_info()