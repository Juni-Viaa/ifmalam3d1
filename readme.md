# ML Dashboard - Machine Learning Training & Analysis Platform

Dashboard aplikasi untuk training dan analisis model Machine Learning dengan visualisasi interaktif.

## 📁 Struktur Project

```
ml-dashboard/
│
├── app.py                      # Main application file
│
├── pages/                      # Page modules
│   ├── __init__.py
│   ├── home.py                # Home page
│   ├── model.py               # Model training page
│   ├── analysis.py            # Analysis page
│   ├── comparison.py          # Model comparison page
│   └── about.py               # About page
│
├── ml/                        # Machine learning modules
│   ├── __init__.py
│   └── model_trainer.py       # Model training logic
│
├── utils/                     # Utility modules
│   ├── __init__.py
│   └── session_manager.py     # Session state management
│
├── styles/                    # Styling modules
│   ├── __init__.py
│   └── custom_css.py          # Custom CSS styling
│
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Clone atau Download Project

```bash
# Clone repository (jika menggunakan git)
git clone <repository-url>
cd ml-dashboard

# Atau download dan extract ZIP file
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Create Required Folders

```bash
# Buat folder jika belum ada
mkdir pages ml utils styles
```

### Step 5: Create __init__.py Files

Buat file `__init__.py` kosong di setiap folder:

```bash
# Windows
type nul > pages\__init__.py
type nul > ml\__init__.py
type nul > utils\__init__.py
type nul > styles\__init__.py

# Linux/Mac
touch pages/__init__.py
touch ml/__init__.py
touch utils/__init__.py
touch styles/__init__.py
```

## 📦 Dependencies

File `requirements.txt`:

```
streamlit>=1.28.0
pandas>=2.0.0
numpy>=1.24.0
scikit-learn>=1.3.0
matplotlib>=3.7.0
openpyxl>=3.1.0
```

## 🎯 Usage

### Running the Application

```bash
streamlit run app.py
```

Aplikasi akan terbuka di browser pada `http://localhost:8501`

### Using the Dashboard

1. **Home Page**
   - Overview aplikasi dan fitur-fitur yang tersedia
   - Status sistem (data loaded, models trained)

2. **Model Page**
   - Upload file Excel (.xlsx)
   - Pilih model ML di sidebar (Linear Regression, Decision Tree, Random Forest)
   - Atur parameter model
   - Train model dengan tombol "Train Model"
   - Lihat hasil evaluasi (MAE, MSE, RMSE, MAPE, R²)

3. **Analisis Page**
   - Pilih model yang sudah dilatih
   - Lihat visualisasi prediksi vs aktual
   - Analisis residuals
   - Lihat feature importance/coefficients
   - Download hasil prediksi

4. **Perbandingan Page**
   - Bandingkan metrik semua model yang sudah dilatih
   - Lihat model terbaik untuk setiap metrik
   - Visualisasi dengan bar chart atau radar chart
   - Perbandingan detail antara 2 model
   - Download tabel perbandingan

5. **Tentang Page**
   - Informasi lengkap aplikasi
   - Panduan penggunaan
   - Persyaratan data
   - FAQ

## 📊 Data Format

File Excel harus memiliki kolom-kolom berikut:

**Features:**
- F1, F2, F3, F4, F5, F6
- P1, P2 (Pressure)
- T1, T2, T3, T4, T5 (Temperature)
- L1 (Load)
- SPF2, SPF3 (Special Features)

**Target:**
- TARGET (nilai yang akan diprediksi)

**Format:**
- Semua kolom harus numerik
- Tidak boleh ada missing values
- Data akan diproses dalam batch 48 baris
- Rata-rata setiap fitur per batch akan dihitung
- Nilai TARGET dari baris terakhir setiap batch digunakan

### Contoh Data

| F1 | F2 | F3 | F4 | F5 | F6 | P1 | P2 | T1 | T2 | T3 | T4 | T5 | L1 | SPF2 | SPF3 | TARGET |
|----|----|----|----|----|----|----|----|----|----|----|----|----|-------|------|------|--------|
| 1.2 | 3.4 | 5.6 | 7.8 | 9.0 | 1.1 | 2.2 | 3.3 | 4.4 | 5.5 | 6.6 | 7.7 | 8.8 | 9.9 | 10.1 | 11.2 | 100.5 |
| ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |

## 🎨 Features

### Model Training
- **Multiple Models**: Linear Regression, Decision Tree, Random Forest
- **Customizable Parameters**: Sesuaikan parameter untuk setiap model
- **Automatic Training**: Train dengan satu klik
- **Model Storage**: Simpan multiple trained models dalam session

### Evaluation Metrics
- MAE (Mean Absolute Error)
- MSE (Mean Squared Error)
- RMSE (Root Mean Squared Error)
- MAPE (Mean Absolute Percentage Error)
- R² Score (Coefficient of Determination)

### Visualizations
- Line charts (Actual vs Predicted)
- Scatter plots
- Residuals analysis
- Feature importance charts
- Radar charts for model comparison

### Model Comparison
- Side-by-side metrics comparison
- Visual comparison with multiple chart types
- Best model recommendations
- Detailed 2-model comparison

## ⚙️ Configuration

### Sidebar Settings

**Model Selection:**
- Linear Regression
- Decision Tree (max_depth, min_samples_split)
- Random Forest (n_estimators, max_depth)

**Training Settings:**
- Test size (10-40%, default 20%)
- Random state (for reproducibility)
- Batch size (default 48 rows)

## 🐛 Troubleshooting

### Common Issues

**Issue: "No module named 'pages'"**
- Solusi: Pastikan semua folder memiliki file `__init__.py`

**Issue: "File tidak bisa diupload"**
- Solusi: Pastikan file dalam format .xlsx dan memiliki semua kolom yang diperlukan

**Issue: "Model training error"**
- Solusi: Check apakah data memiliki missing values atau format yang salah

**Issue: "Page tidak ditemukan"**
- Solusi: Pastikan semua file page ada di folder `pages/`

## 📝 Development

### Adding New Models

1. Edit `ml/model_trainer.py`
2. Tambahkan model baru di method `get_model()`
3. Update sidebar di `app.py` untuk menambah model option
4. Test training dan evaluation

### Customizing Styles

Edit `styles/custom_css.py` untuk mengubah:
- Colors
- Fonts
- Layouts
- Animations

### Adding New Pages

1. Buat file baru di folder `pages/` (e.g., `new_page.py`)
2. Implement function `show()`
3. Import di `app.py`
4. Tambahkan navigation button
5. Add routing logic

## 📄 License

Project ini dibuat untuk keperluan pembelajaran dan analisis data.

## 🤝 Contributing

Untuk kontribusi atau saran improvement:
1. Fork repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

## 📧 Contact

Untuk pertanyaan atau dukungan, hubungi tim pengembang.

---

**Made with ❤️ using Streamlit**