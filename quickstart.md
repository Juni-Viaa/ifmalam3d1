# 🚀 Quick Start Guide - ML Dashboard

Panduan lengkap untuk setup dan menjalankan aplikasi ML Dashboard.

## 📋 Prerequisites

Sebelum memulai, pastikan Anda sudah menginstall:

- **Python 3.8+** - [Download Python](https://www.python.org/downloads/)
- **pip** - Biasanya sudah terinstall dengan Python
- **Text Editor** - VS Code, PyCharm, atau editor favorit Anda

## 🏗️ Step-by-Step Installation

### Step 1: Persiapan Folder

Buat struktur folder project seperti berikut:

```
ml-dashboard/
│
├── app.py
├── requirements.txt
├── README.md
│
├── pages/
│   ├── __init__.py
│   ├── home.py
│   ├── model.py
│   ├── analysis.py
│   ├── comparison.py
│   └── about.py
│
├── ml/
│   ├── __init__.py
│   └── model_trainer.py
│
├── utils/
│   ├── __init__.py
│   └── session_manager.py
│
└── styles/
    ├── __init__.py
    └── custom_css.py
```

**Cara cepat membuat folder:**

```bash
# Windows (Command Prompt)
mkdir ml-dashboard
cd ml-dashboard
mkdir pages ml utils styles

# Linux/Mac (Terminal)
mkdir -p ml-dashboard/{pages,ml,utils,styles}
cd ml-dashboard
```

### Step 2: Copy File-file

Copy semua file yang telah disediakan ke dalam folder yang sesuai:

1. **app.py** → Root folder
2. **requirements.txt** → Root folder
3. **README.md** → Root folder
4. File-file di **pages/** → folder pages/
5. File-file di **ml/** → folder ml/
6. File-file di **utils/** → folder utils/
7. File-file di **styles/** → folder styles/

### Step 3: Buat Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

Anda akan melihat `(venv)` di awal command prompt Anda.

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

Tunggu hingga semua package terinstall. Ini akan menginstall:
- streamlit
- pandas
- numpy
- scikit-learn
- matplotlib
- openpyxl

### Step 5: Verifikasi Instalasi

Check apakah semua package terinstall dengan benar:

```bash
pip list
```

Anda harus melihat semua package yang ada di requirements.txt.

### Step 6: Jalankan Aplikasi

```bash
streamlit run app.py
```

Browser Anda akan otomatis membuka aplikasi di `http://localhost:8501`

## 🎯 First Time Usage

### 1. Persiapkan Data Excel

Buat file Excel dengan format berikut:

**Nama kolom yang diperlukan:**
- F1, F2, F3, F4, F5, F6
- P1, P2
- T1, T2, T3, T4, T5
- L1
- SPF2, SPF3
- TARGET

**Contoh data:**

| F1  | F2  | F3  | F4  | F5  | F6  | P1  | P2  | T1  | T2  | T3  | T4  | T5  | L1  | SPF2 | SPF3 | TARGET |
|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|------|------|--------|
| 1.2 | 3.4 | 5.6 | 7.8 | 9.0 | 1.1 | 2.2 | 3.3 | 4.4 | 5.5 | 6.6 | 7.7 | 8.8 | 9.9 | 10.1 | 11.2 | 100.5  |
| 1.3 | 3.5 | 5.7 | 7.9 | 9.1 | 1.2 | 2.3 | 3.4 | 4.5 | 5.6 | 6.7 | 7.8 | 8.9 | 9.8 | 10.2 | 11.3 | 101.2  |
| ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ...  | ...  | ...    |

**Catatan penting:**
- Minimum 96 baris data (2 batch × 48 rows)
- Semua kolom harus berisi angka (numerik)
- Tidak boleh ada cell kosong
- Simpan sebagai .xlsx

### 2. Workflow Dasar

**A. Home Page**
- Baca overview aplikasi
- Check status sistem

**B. Model Page**
1. Pilih model di sidebar (Linear Regression, Decision Tree, atau Random Forest)
2. Atur parameter model jika perlu
3. Upload file Excel Anda
4. Klik "Train Model"
5. Lihat hasil evaluasi

**C. Train Multiple Models**
1. Pilih model berbeda di sidebar
2. Upload file yang sama
3. Train model lagi
4. Ulangi untuk semua model yang ingin dibandingkan

**D. Analysis Page**
1. Pilih model yang ingin dianalisis
2. Lihat visualisasi prediksi
3. Analisis feature importance
4. Download hasil jika perlu

**E. Comparison Page**
1. Bandingkan semua model yang sudah dilatih
2. Lihat model terbaik
3. Pilih 2 model untuk perbandingan detail
4. Download tabel perbandingan

## 🛠️ Troubleshooting

### Problem: Import Error

**Error:**
```
ModuleNotFoundError: No module named 'streamlit'
```

**Solusi:**
```bash
pip install -r requirements.txt
```

### Problem: Page Not Found

**Error:**
```
ModuleNotFoundError: No module named 'pages'
```

**Solusi:**
Pastikan semua folder memiliki file `__init__.py`

```bash
# Windows
type nul > pages\__init__.py
type nul > ml\__init__.py
type nul > utils\__init__.py
type nul > styles\__init__.py

# Linux/Mac
touch pages/__init__.py ml/__init__.py utils/__init__.py styles/__init__.py
```

### Problem: File Upload Error

**Error:**
```
Error saat memproses file
```

**Solusi:**
1. Check format file (.xlsx)
2. Pastikan semua kolom ada
3. Check tidak ada missing values
4. Pastikan semua data numerik

### Problem: Training Error

**Error:**
```
Error saat training model
```

**Solusi:**
1. Check minimum 96 baris data
2. Pastikan tidak ada nilai non-numerik
3. Check tidak ada nilai infinity atau NaN
4. Coba dengan parameter default terlebih dahulu

### Problem: Port Already in Use

**Error:**
```
Address already in use
```

**Solusi:**
```bash
# Gunakan port berbeda
streamlit run app.py --server.port 8502
```

## 📊 Sample Data Generator

Jika Anda belum punya data, buat sample data dengan Python:

```python
import pandas as pd
import numpy as np

# Set random seed untuk reproducibility
np.random.seed(42)

# Generate 480 rows (10 batches)
n_rows = 480

data = {
    'F1': np.random.uniform(1, 10, n_rows),
    'F2': np.random.uniform(1, 10, n_rows),
    'F3': np.random.uniform(1, 10, n_rows),
    'F4': np.random.uniform(1, 10, n_rows),
    'F5': np.random.uniform(1, 10, n_rows),
    'F6': np.random.uniform(1, 10, n_rows),
    'P1': np.random.uniform(10, 50, n_rows),
    'P2': np.random.uniform(10, 50, n_rows),
    'T1': np.random.uniform(20, 100, n_rows),
    'T2': np.random.uniform(20, 100, n_rows),
    'T3': np.random.uniform(20, 100, n_rows),
    'T4': np.random.uniform(20, 100, n_rows),
    'T5': np.random.uniform(20, 100, n_rows),
    'L1': np.random.uniform(100, 500, n_rows),
    'SPF2': np.random.uniform(1, 5, n_rows),
    'SPF3': np.random.uniform(1, 5, n_rows),
    'TARGET': np.random.uniform(50, 150, n_rows)
}

df = pd.DataFrame(data)
df.to_excel('sample_data.xlsx', index=False)
print("Sample data created: sample_data.xlsx")
```

Jalankan script di atas untuk generate sample data.

## 💡 Tips & Tricks

### 1. Keyboard Shortcuts

- `Ctrl + C` (di terminal) - Stop aplikasi
- `R` - Rerun aplikasi (di browser)
- `C` - Clear cache

### 2. Performance Tips

- Gunakan data dengan jumlah batch yang wajar (< 100 batch)
- Clear trained models jika tidak digunakan
- Refresh page jika terasa lambat

### 3. Best Practices

- **Mulai dengan Linear Regression** untuk baseline
- **Train multiple models** untuk comparison
- **Eksperimen dengan parameters** untuk hasil optimal
- **Save predictions** sebelum train model baru
- **Document parameters** yang memberikan hasil terbaik

## 🔄 Updating the Application

Jika ada update pada kode:

```bash
# Stop aplikasi (Ctrl + C)
# Pull update atau copy file baru
# Restart aplikasi
streamlit run app.py
```

Streamlit akan otomatis detect perubahan dan reload.