# 💾 Model Persistence Guide

## Overview

Fitur Model Persistence memungkinkan model yang sudah dilatih untuk **tersimpan secara permanen** di disk, sehingga tidak hilang ketika aplikasi Streamlit di-restart.

## 🎯 Fitur Utama

### 1. **Auto-Save**
- Model otomatis disimpan ke disk setelah training berhasil
- Tidak perlu klik tombol save manual
- Metadata (metrics, parameters) juga disimpan

### 2. **Auto-Load**
- Saat aplikasi dijalankan ulang, model otomatis dimuat dari disk
- Model langsung tersedia tanpa perlu training ulang
- Loading progress ditampilkan saat startup

### 3. **Storage Management**
- Lihat berapa banyak model tersimpan
- Cek ukuran storage yang digunakan
- Lokasi penyimpanan yang jelas

### 4. **Individual Control**
- Load/unload model tertentu dari memory
- Delete model tertentu dari disk
- Clear all models sekaligus

## 📁 Struktur Penyimpanan

```
ml-dashboard/
└── saved_models/
    ├── models/
    │   ├── Linear_Regression.pkl
    │   ├── Decision_Tree.pkl
    │   └── Random_Forest.pkl
    └── metadata/
        ├── Linear_Regression.json
        ├── Decision_Tree.json
        └── Random_Forest.json
```

### File `.pkl` (Model Object)
Berisi trained model object dari scikit-learn:
- Model weights/coefficients
- Model structure
- Trained parameters

### File `.json` (Metadata)
Berisi informasi tentang model:
```json
{
    "model_name": "Linear Regression",
    "metrics": {
        "MAE": 0.1234,
        "MSE": 0.5678,
        "RMSE": 0.7890,
        "MAPE": 5.67,
        "R2": 0.95
    },
    "params": {
        "fit_intercept": true
    },
    "predictions": {
        "y_pred": [...],
        "y_test": [...],
        "feature_importance": {...}
    },
    "saved_at": "2024-01-15 10:30:45"
}
```

## 🔄 Workflow

### Training & Saving
```
1. User uploads data
   ↓
2. User trains model
   ↓
3. Model saves to session_state ✅
   ↓
4. Model auto-saves to disk 💾
   ↓
5. Success message shown
```

### Loading on Restart
```
1. User runs: streamlit run app.py
   ↓
2. App initializes
   ↓
3. Check saved_models/ folder
   ↓
4. Load all .pkl files 📥
   ↓
5. Load metadata from .json files
   ↓
6. Populate session_state
   ↓
7. Models ready to use! ✅
```

## 💻 Usage Examples

### Halaman Model
```python
# After training, model is automatically saved
# You'll see: "✅ Model Linear Regression berhasil dilatih dan disimpan ke disk!"

# Clear all models (from memory AND disk)
# Click "🗑️ Clear All Models" button
```

### Halaman Saved Models
```python
# View all saved models
# See storage info, saved date, metrics

# Load specific model to memory
# Click "📥 Load to Memory"

# Delete specific model from disk
# Click "🗑️ Delete from Disk"

# Reload all models from disk
# Click "🔄 Reload All Models"
```

## ⚙️ Configuration

### Change Storage Location
Edit `utils/model_persistence.py`:

```python
# Default location
persistence = ModelPersistence(base_dir="saved_models")

# Custom location
persistence = ModelPersistence(base_dir="/path/to/custom/folder")
```

### Disable Auto-Load
Edit `app.py`:

```python
# Comment out these lines:
# if "models_loaded" not in st.session_state:
#     with st.spinner("Memuat saved models..."):
#         loaded, total = st.session_state.model_persistence.load_all_models()
#         if loaded > 0:
#             st.success(f"✅ {loaded} model(s) berhasil dimuat dari disk!")
#         st.session_state.models_loaded = True
```

### Disable Auto-Save
Edit `pages/model.py`:

```python
# Comment out these lines:
# success, message = st.session_state.model_persistence.save_model(
#     current_model, 
#     model_data
# )
```

## 🔒 Security Considerations

### Safe Practices
✅ **DO:**
- Backup `saved_models/` folder regularly
- Use `.gitignore` to exclude large model files from git
- Check disk space periodically
- Delete old/unused models

❌ **DON'T:**
- Share `.pkl` files from untrusted sources
- Manually edit `.json` metadata files
- Delete `saved_models/` folder while app is running
- Store sensitive data in model metadata

### Pickle Security
⚠️ **Warning:** Pickle files can execute arbitrary code. Only load models you trust!

```python
# Safe: Models trained by your own app
model = persistence.load_model("Linear Regression")

# Unsafe: Models from unknown sources
# Don't load random .pkl files!
```

## 🐛 Troubleshooting

### Issue: Models not loading on restart

**Possible Causes:**
1. `saved_models/` folder deleted
2. Permissions issue
3. Corrupted files

**Solution:**
```python
# Check if folder exists
import os
os.path.exists('saved_models/models/')
os.path.exists('saved_models/metadata/')

# Recreate folders
os.makedirs('saved_models/models/', exist_ok=True)
os.makedirs('saved_models/metadata/', exist_ok=True)
```

### Issue: Model loaded but predictions don't work

**Possible Causes:**
1. Model trainer code changed
2. Scikit-learn version mismatch
3. Feature names changed

**Solution:**
- Delete old models
- Retrain with new code
- Check scikit-learn version consistency

### Issue: Storage full

**Solution:**
```python
# Check storage
storage_info = persistence.get_storage_info()
print(f"Storage used: {storage_info['total_size_mb']} MB")

# Delete old models
persistence.delete_model("old_model_name")

# Or clear all
persistence.clear_all_saved_models()
```

### Issue: Import Error

**Error:**
```
ImportError: cannot import name 'ModelPersistence' from 'utils'
```

**Solution:**
```bash
# Make sure __init__.py includes ModelPersistence
# Check utils/__init__.py contains:
from .model_persistence import ModelPersistence
```

## 📊 Performance Impact

### Saving (Auto-save after training)
- **Time:** ~0.5-2 seconds per model
- **Storage:** 1-10 MB per model (depends on complexity)
- **Impact:** Minimal, happens in background

### Loading (Auto-load on startup)
- **Time:** ~0.5-1 second per model
- **Memory:** Same as training time
- **Impact:** One-time delay on startup

### Recommendations
- Keep < 50 models saved for optimal performance
- Delete old/unused models regularly
- Use SSD for faster load times

## 🔄 Migration Guide

### From Non-Persistent to Persistent

**Before (No Persistence):**
```python
# Models lost on restart
st.session_state.trained_models = {}
```

**After (With Persistence):**
```python
# Models persist across restarts
persistence.save_model(model_name, model_data)
```

**Migration Steps:**
1. Add `utils/model_persistence.py`
2. Update `utils/__init__.py`
3. Update `app.py` with auto-load
4. Update `pages/model.py` with auto-save
5. Retrain all models (they'll auto-save)

### Backup Existing Models

```bash
# Before updating, backup session state models
# Option 1: Export to pickle manually
python -c "
import streamlit as st
import pickle
# Save current models before update
"

# Option 2: Screenshot metrics for reference
```

## 📚 API Reference

### ModelPersistence Class

```python
class ModelPersistence:
    def __init__(self, base_dir="saved_models"):
        """Initialize with custom base directory"""
        
    def save_model(self, model_name, model_data):
        """Save model and metadata to disk"""
        # Returns: (success: bool, message: str)
        
    def load_model(self, model_name):
        """Load model from disk"""
        # Returns: model_data dict or None
        
    def delete_model(self, model_name):
        """Delete model from disk"""
        # Returns: (success: bool, message: str)
        
    def list_saved_models(self):
        """List all saved models"""
        # Returns: list of model info dicts
        
    def load_all_models(self):
        """Load all saved models to session state"""
        # Returns: (loaded_count: int, total_count: int)
        
    def clear_all_saved_models(self):
        """Delete all models from disk"""
        # Returns: (success: bool, message: str)
        
    def get_storage_info(self):
        """Get storage usage information"""
        # Returns: dict with size and count info
```

## 💡 Best Practices

1. **Regular Cleanup**
   - Delete old models monthly
   - Keep only best performing models

2. **Naming Convention**
   - Use descriptive names
   - Include date/version if needed
   - Example: "LinearReg_v2_2024"

3. **Backup Strategy**
   - Weekly backup of `saved_models/`
   - Store backups off-site
   - Test restore process

4. **Version Control**
   - Git ignore `saved_models/` for large files
   - Or use Git LFS for model versioning
   - Document model versions in README

5. **Monitoring**
   - Check storage usage regularly
   - Monitor load times
   - Log errors to file

## 🎓 Advanced Tips

### Custom Serialization

For large models, use compression:

```python
import gzip
import pickle

# Save with compression
with gzip.open('model.pkl.gz', 'wb') as f:
    pickle.dump(model, f)

# Load compressed
with gzip.open('model.pkl.gz', 'rb') as f:
    model = pickle.load(f)
```

### Cloud Storage Integration

Integrate with S3/GCS:

```python
# Save to cloud storage
import boto3

s3 = boto3.client('s3')
s3.upload_file('saved_models/models/model.pkl', 
               'bucket-name', 'models/model.pkl')
```

### Model Versioning

Track model versions:

```python
metadata = {
    'version': '1.0.0',
    'created_at': datetime.now(),
    'trained_by': 'user@example.com',
    'git_commit': 'abc123',
    ...
}
```

## 📞 Support

Jika mengalami masalah dengan Model Persistence:

1. Check logs di terminal
2. Verify file permissions
3. Check disk space
4. Review troubleshooting section
5. Contact development team

---

**Last Updated:** 2024
**Version:** 1.0.0