# 🖥️ PC Performance Benchmarking Suite (SSC Project)
**Bogdan Alexandru Birlea | Grupa 30234 | An Academic 2023-2027**

---

## 📖 1. Introducere & Obiective
Acest proiect reprezintă o suită completă de benchmark pentru evaluarea performanței sistemului, utilizând **Python** pentru portabilitate. Obiectivul principal este colectarea datelor hardware (CPU, RAM, Disk) și măsurarea timpilor de execuție pentru operații critice.

### Obiective Specifice:
* **Hardware Discovery:** Identificarea modelului CPU, frecvenței și nucleelor folosind instrucțiunea hardware CPUID.
* **ALU & FPU Testing:** Evaluarea performanței pe numere întregi (Ciurul lui Eratostene) și virgulă mobilă (Seria Leibniz).
* **I/O Analysis:** Teste de citire/scriere fișiere pentru evaluarea vitezei secvențiale și a IOPS.
* **Multi-core Stress:** Aplicarea paralelizării prin multiprocessing pentru a ocoli limitările GIL.

---

## 🏗️ 2. Arhitectură și Design

Aplicația urmează o arhitectură modulară, decuplând complet interfața grafică de logica de testare.

### Module Principale:
* **`main.py`**: Launcher-ul aplicației.
* **`benchmark_gui.py`**: Interfața grafică realizată în Tkinter cu monitorizare live via Matplotlib.
* **`hardware_info.py`**: Colectarea datelor de sistem (psutil & py-cpuinfo).
* **`multi_core.py`**: Modulul de stres CPU care utilizează toate nucleele logice disponibile.

---

## 🧪 3. Metodologie de Calcul

### 🔢 3.1 Calcul Integer (ALU)
Solicită intensiv Unitatea Aritmetică-Logică prin operații modulo și împărțiri, folosind un algoritm de filtrare a numerelor prime.

### 🥧 3.2 Calcul Float (FPU)
Solicită Unitatea de Virgulă Mobilă prin calculul aproximat al lui $\pi$ pe parcursul a milioane de iterații matematice.

### 💾 3.3 Disk I/O
Măsoară latența și lățimea de bandă a stocării, fiind cel mai relevant indicator pentru viteza percepută a sistemului de operare.

---

## 📊 4. Sistemul de Scor (Relativ la Baseline)

Scorul este calculat prin raportare la un sistem **Etalon (1000 puncte)**: AMD Ryzen 7 3750H, 8 nuclee, 32GB RAM.

| Interval Scor | Categorie | Descriere Tipică |
| :--- | :--- | :--- |
| **< 700** | Entry Level | Laptopuri office, procesoare tip Celeron/Pentium. |
| **700 - 1100** | Mainstream | Performanță echilibrată (Referința proiectului). |
| **1100 - 3000** | Performance | PC-uri de gaming sau stații de lucru moderne. |
| **> 3000** | High-End | Workstations profesionale (i9, Ryzen 9), SSD NVMe Gen4. |

---

## 🔬 5. Rezultate Experimentale (Validare)

Validarea sistemului de notare pe configurații hardware reale extrase din documentație:

| Utilizator | Model Procesor | Nuclee | RAM | Scor Total |
| :--- | :--- | :--- | :--- | :--- |
| **PC1** | Intel i9-13900K | 24/32 | 32GB | **5552** |
| **PC2** | AMD Ryzen 7 7745HX | 8/16 | 32GB | **4689** |
| **PC4** | AMD Ryzen 7 5800H | 8/16 | 16GB | **2491** |
| **PC6** | **AMD Ryzen 7 3750H** | **4/8** | **32GB** | **1190** |

---

## 🚦 6. Ghid de Rulare

### Varianta Standalone
Aplicația poate fi rulată fără Python instalat, folosind executabilul portabil:
1. Navighează în folderul `Dist`.
2. Deschide `BenchmarkApp.exe`.

### Varianta Development
1. `pip install matplotlib psutil py-cpuinfo pillow`
2. `python Main.py`
