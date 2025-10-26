import os
import pickle
import json
from datetime import datetime
import streamlit as st

class ModelPersistence:
    """Class untuk menyimpan dan memuat model ke/dari disk"""
    
    def __init__(self, base_dir="saved_models"):
        self.base_dir = base_dir
        self.models_dir = os.path.join(base_dir, "models")
        self.metadata_dir = os.path.join(base_dir, "metadata")
        self._ensure_directories()
    
    def _ensure_directories(self):
        """Buat direktori jika belum ada"""
        os.makedirs(self.models_dir, exist_ok=True)
        os.makedirs(self.metadata_dir, exist_ok=True)
    
    def _sanitize_filename(self, name):
        """Bersihkan nama file dari karakter tidak valid"""
        return name.replace(" ", "_").replace("/", "_").replace("\\", "_")
    
    def save_model(self, model_name, model_data):
        """
        Simpan model dan metadata ke disk
        
        Args:
            model_name: Nama model
            model_data: Dictionary berisi model, metrics, predictions, params
        """
        try:
            sanitized_name = self._sanitize_filename(model_name)
            
            # Simpan model object
            model_path = os.path.join(self.models_dir, f"{sanitized_name}.pkl")
            with open(model_path, 'wb') as f:
                pickle.dump(model_data['model'], f)
            
            # Simpan metadata (metrics, params, predictions)
            metadata = {
                'model_name': model_name,
                'metrics': model_data['metrics'],
                'params': model_data['params'],
                'predictions': {
                    'y_pred': model_data['predictions']['y_pred'].tolist() if hasattr(model_data['predictions']['y_pred'], 'tolist') else list(model_data['predictions']['y_pred']),
                    'y_test': model_data['predictions']['y_test'].tolist() if hasattr(model_data['predictions']['y_test'], 'tolist') else list(model_data['predictions']['y_test']),
                    'feature_importance': model_data['predictions'].get('feature_importance', {})
                },
                'saved_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            metadata_path = os.path.join(self.metadata_dir, f"{sanitized_name}.json")
            with open(metadata_path, 'w') as f:
                json.dump(metadata, f, indent=4)
            
            return True, f"Model '{model_name}' berhasil disimpan!"
            
        except Exception as e:
            return False, f"Error menyimpan model: {str(e)}"
    
    def load_model(self, model_name):
        """
        Muat model dan metadata dari disk
        
        Args:
            model_name: Nama model yang akan dimuat
            
        Returns:
            Dictionary berisi model, metrics, predictions, params atau None
        """
        try:
            sanitized_name = self._sanitize_filename(model_name)
            
            # Load model object
            model_path = os.path.join(self.models_dir, f"{sanitized_name}.pkl")
            if not os.path.exists(model_path):
                return None
            
            with open(model_path, 'rb') as f:
                model = pickle.load(f)
            
            # Load metadata
            metadata_path = os.path.join(self.metadata_dir, f"{sanitized_name}.json")
            if not os.path.exists(metadata_path):
                return None
            
            with open(metadata_path, 'r') as f:
                metadata = json.load(f)
            
            # Reconstruct model_data
            import numpy as np
            model_data = {
                'model': model,
                'metrics': metadata['metrics'],
                'params': metadata['params'],
                'predictions': {
                    'y_pred': np.array(metadata['predictions']['y_pred']),
                    'y_test': np.array(metadata['predictions']['y_test']),
                    'feature_importance': metadata['predictions'].get('feature_importance', {})
                },
                'saved_at': metadata.get('saved_at', 'Unknown')
            }
            
            return model_data
            
        except Exception as e:
            st.error(f"Error memuat model '{model_name}': {str(e)}")
            return None
    
    def delete_model(self, model_name):
        """Hapus model dari disk"""
        try:
            sanitized_name = self._sanitize_filename(model_name)
            
            model_path = os.path.join(self.models_dir, f"{sanitized_name}.pkl")
            metadata_path = os.path.join(self.metadata_dir, f"{sanitized_name}.json")
            
            if os.path.exists(model_path):
                os.remove(model_path)
            
            if os.path.exists(metadata_path):
                os.remove(metadata_path)
            
            return True, f"Model '{model_name}' berhasil dihapus!"
            
        except Exception as e:
            return False, f"Error menghapus model: {str(e)}"
    
    def list_saved_models(self):
        """Dapatkan list semua model yang tersimpan"""
        try:
            models = []
            
            if not os.path.exists(self.metadata_dir):
                return models
            
            for filename in os.listdir(self.metadata_dir):
                if filename.endswith('.json'):
                    metadata_path = os.path.join(self.metadata_dir, filename)
                    
                    with open(metadata_path, 'r') as f:
                        metadata = json.load(f)
                    
                    models.append({
                        'name': metadata['model_name'],
                        'saved_at': metadata.get('saved_at', 'Unknown'),
                        'metrics': metadata['metrics']
                    })
            
            return models
            
        except Exception as e:
            st.error(f"Error membaca saved models: {str(e)}")
            return []
    
    def load_all_models(self):
        """Muat semua model yang tersimpan ke session state"""
        saved_models = self.list_saved_models()
        loaded_count = 0
        
        for model_info in saved_models:
            model_name = model_info['name']
            
            # Cek apakah model sudah ada di session state
            if model_name not in st.session_state.trained_models:
                model_data = self.load_model(model_name)
                
                if model_data:
                    st.session_state.trained_models[model_name] = model_data
                    loaded_count += 1
        
        return loaded_count, len(saved_models)
    
    def clear_all_saved_models(self):
        """Hapus semua model yang tersimpan"""
        try:
            import shutil
            
            if os.path.exists(self.base_dir):
                shutil.rmtree(self.base_dir)
                self._ensure_directories()
            
            return True, "Semua saved models berhasil dihapus!"
            
        except Exception as e:
            return False, f"Error menghapus saved models: {str(e)}"
    
    def get_storage_info(self):
        """Dapatkan informasi storage"""
        try:
            total_size = 0
            model_count = 0
            
            if os.path.exists(self.base_dir):
                for dirpath, dirnames, filenames in os.walk(self.base_dir):
                    for filename in filenames:
                        filepath = os.path.join(dirpath, filename)
                        total_size += os.path.getsize(filepath)
                        
                        if filename.endswith('.pkl'):
                            model_count += 1
            
            # Convert to MB
            size_mb = total_size / (1024 * 1024)
            
            return {
                'total_size_mb': round(size_mb, 2),
                'model_count': model_count,
                'base_dir': self.base_dir
            }
            
        except Exception as e:
            return {
                'total_size_mb': 0,
                'model_count': 0,
                'base_dir': self.base_dir,
                'error': str(e)
            }