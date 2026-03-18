# 🖥️ PC Performance Benchmarking Suite (SSC Project)
**Bogdan Alexandru Birlea | Grupa 30234 | [cite_start]An Academic 2023-2027** [cite: 7, 8]

---

## 📖 1. Introducere & Obiective
[cite_start]Acest proiect reprezintă o suită completă de benchmark pentru evaluarea performanței sistemului, utilizând **Python** pentru portabilitate[cite: 15]. [cite_start]Obiectivul principal este colectarea datelor hardware (CPU, RAM, Disk) și măsurarea timpilor de execuție pentru operații critice de calcul numeric și I/O[cite: 16].

### Obiective Specifice:
* **Hardware Discovery:** Identificarea modelului CPU, frecvenței și nucleelor[cite: 18].
* [cite_start]**ALU & FPU Testing:** Evaluarea performanței pe numere întregi și virgulă mobilă[cite: 21].
* [cite_start]**I/O Analysis:** Teste de citire/scriere fișiere pentru evaluarea discului[cite: 22].
* **Multi-core Stress:** Aplicarea paralelizării pentru analiza impactului nucleelor multiple[cite: 23].

---

## 🏗️ 2. Arhitectură și Design Initial

Aplicația urmează o **arhitectură modulară**, decuplând complet logica de prezentare (GUI) de logica de business (testele)[cite: 134].

### Module Principale:
* [cite_start]**`main.py`**: Punctul de intrare care inițializează interfața grafică[cite: 138, 140].
* [cite_start]**`benchmark_gui.py`**: Gestionează evenimentele utilizatorului și afișarea graficelor `matplotlib` în timp real[cite: 141, 146].
* [cite_start]**`hardware_info.py`**: Extrage date folosind instrucțiunea hardware **CPUID** (x86) și biblioteca `psutil`[cite: 85, 86].
* **`multi_core.py`**: Utilizează `multiprocessing` pentru a ocoli limitarea **GIL (Global Interpreter Lock)** din Python, permițând stresarea simultană a tuturor nucleelor[cite: 271, 276].

---

## 🧪 3. Metodologie și Algoritmi

### 🔢 3.1 Calcul Integer (ALU) - Ciurul lui Eratostene
[cite_start]Algoritmul filtrează numerele prime prin eliminarea multiplilor, solicitând intensiv operațiile de tip modulo și împărțirile întregi[cite: 93, 98].

### 🥧 3.2 Calcul Float (FPU) - Seria Leibniz
[cite_start]Calculul constantei $\pi$ prin milioane de iterații de sume alternante de fracții, solicitând la maximum Unitatea de Virgulă Mobilă (FPU) a procesorului[cite: 101, 102].

### 💾 3.3 Disk I/O (Sequential vs Random)
* **Secvențial:** Citire/scriere blocuri de 4MB (simulează transferul de fișiere mari)[cite: 163, 350].
* [cite_start]**Aleatoriu (IOPS):** Operații de 4KB la poziții random (simulează pornirea sistemului/aplicațiilor)[cite: 164, 353].

---

## 📊 4. Sistemul de Calcul al Scorului (Baseline)

[cite_start]Punctajul este calibrat față de un **sistem de referință (Baseline)** evaluat la **1000 de puncte**[cite: 227, 230].

[cite_start]**Specificații Baseline:** AMD Ryzen 7 3750H, 8 Nuclee Logice, 32GB RAM[cite: 232, 233, 234].

### Grila de Interpretare:
| Scor | Categorie | Descriere |
| :--- | :--- | :--- |
| **< 700** | Entry Level | [cite_start]Laptopuri vechi, procesoare Celeron/Pentium[cite: 263]. |
| **700 - 1100** | Mainstream | [cite_start]Sistemul Etalon (Ryzen 7 / i5 gen 9-10)[cite: 263]. |
| **1100 - 3000** | Performance | [cite_start]Desktop-uri moderne, SSD NVMe rapide[cite: 263]. |
| **> 3000** | High-End | [cite_start]Stații de lucru (i9, Ryzen 9), randări 4K[cite: 265]. |

---

## 🔬 5. Rezultate Experimentale & Validare

[cite_start]Validarea sistemului de notare pe diverse configurații hardware reale:

| Utilizator | CPU | Nuclee | RAM | Disc | **Scor Total** |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **PC1** | i9-13900K | 24/32 | 32GB | SSD | **5552** |
| **PC2** | Ryzen 7 7745HX | 8/16 | 32GB | SSD | **4689** |
| **PC4** | Ryzen 7 5800H | 8/16 | 16GB | SSD | **2491** |
| **PC6** | **Ryzen 7 3750H** | **4/8** | **32GB** | **SSD+HDD** | **1190** |

---

## 🚦 6. Instalare și Rulare

### Varianta Standalone (Recomandată)
[cite_start]Aplicația a fost compilată folosind `PyInstaller` într-un pachet executabil portabil (`.exe`) care conține toate dependențele (Plug-and-Play)[cite: 378, 382].
1. [cite_start]Navighează în folderul `Dist`[cite: 384].
2. [cite_start]Execută `BenchmarkApp.exe`[cite: 385].

### Varianta pentru Dezvoltatori
1. [cite_start]Necesită Python 3.8+[cite: 392].
2. [cite_start]Instalare librării: `pip install matplotlib psutil py-cpuinfo pillow`[cite: 393].
3. [cite_start]Rulare: `python Main.py`[cite: 394].

---

## 📑 7. Bibliografie
* Python Software Foundation, "timeit" Documentation[cite: 427, 429].
* [cite_start]psutil project, https://psutil.readthedocs.io[cite: 430].
* [cite_start]Hangan Anca, "Structure of Computer Systems", UTCN[cite: 435].
