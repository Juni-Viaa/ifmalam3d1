import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler

class DataPreprocessor:
    """Class untuk preprocessing data termasuk normalisasi"""
    
    def __init__(self):
        self.scaler = None
        self.scaler_type = None
        self.is_fitted = False
        
    def fit_scaler(self, X, scaler_type='standard'):
        """
        Fit scaler pada data training
        
        Args:
            X: Training data (DataFrame atau array)
            scaler_type: 'standard', 'minmax', 'robust', atau 'none'
        """
        # Handle 'none' case
        if scaler_type == 'none' or not scaler_type:
            self.scaler_type = 'none'
            self.scaler = None
            self.is_fitted = False
            return self
        
        self.scaler_type = scaler_type.lower().strip()
        
        if self.scaler_type == 'standard':
            self.scaler = StandardScaler()
        elif self.scaler_type == 'minmax':
            self.scaler = MinMaxScaler()
        elif self.scaler_type == 'robust':
            self.scaler = RobustScaler()
        else:
            raise ValueError(f"Unknown scaler type: {scaler_type}. Use 'standard', 'minmax', or 'robust'")
        
        self.scaler.fit(X)
        self.is_fitted = True
        
        return self
    
    def transform(self, X):
        """
        Transform data menggunakan fitted scaler
        
        Args:
            X: Data yang akan ditransform
            
        Returns:
            Transformed data (DataFrame dengan nama kolom sama)
        """
        if not self.is_fitted:
            raise ValueError("Scaler belum di-fit! Gunakan fit_scaler() terlebih dahulu.")
        
        # Keep column names if DataFrame
        if isinstance(X, pd.DataFrame):
            columns = X.columns
            X_scaled = self.scaler.transform(X)
            return pd.DataFrame(X_scaled, columns=columns, index=X.index)
        else:
            return self.scaler.transform(X)
    
    def fit_transform(self, X, scaler_type='standard'):
        """
        Fit dan transform data sekaligus
        
        Args:
            X: Training data
            scaler_type: 'standard', 'minmax', atau 'robust'
            
        Returns:
            Transformed data
        """
        self.fit_scaler(X, scaler_type)
        return self.transform(X)
    
    def inverse_transform(self, X):
        """
        Kembalikan data ke skala asli
        
        Args:
            X: Scaled data
            
        Returns:
            Original scale data
        """
        if not self.is_fitted:
            raise ValueError("Scaler belum di-fit!")
        
        if isinstance(X, pd.DataFrame):
            columns = X.columns
            X_original = self.scaler.inverse_transform(X)
            return pd.DataFrame(X_original, columns=columns, index=X.index)
        else:
            return self.scaler.inverse_transform(X)
    
    def get_scaler_info(self):
        """Dapatkan informasi tentang scaler"""
        if not self.is_fitted:
            return {
                'fitted': False,
                'scaler_type': None
            }
        
        info = {
            'fitted': True,
            'scaler_type': self.scaler_type
        }
        
        # Add scaler-specific info
        if self.scaler_type == 'standard':
            info['mean'] = self.scaler.mean_.tolist() if hasattr(self.scaler, 'mean_') else None
            info['std'] = self.scaler.scale_.tolist() if hasattr(self.scaler, 'scale_') else None
        elif self.scaler_type == 'minmax':
            info['min'] = self.scaler.data_min_.tolist() if hasattr(self.scaler, 'data_min_') else None
            info['max'] = self.scaler.data_max_.tolist() if hasattr(self.scaler, 'data_max_') else None
        elif self.scaler_type == 'robust':
            info['center'] = self.scaler.center_.tolist() if hasattr(self.scaler, 'center_') else None
            info['scale'] = self.scaler.scale_.tolist() if hasattr(self.scaler, 'scale_') else None
        
        return info
    
    def reset(self):
        """Reset scaler"""
        self.scaler = None
        self.scaler_type = None
        self.is_fitted = False


def get_scaler_description(scaler_type):
    """Dapatkan deskripsi scaler"""
    descriptions = {
        'none': {
            'name': 'No Normalization',
            'description': 'Data tidak dinormalisasi. Gunakan untuk tree-based models (Decision Tree, Random Forest).',
            'formula': 'X_scaled = X',
            'best_for': ['Decision Tree', 'Random Forest']
        },
        'standard': {
            'name': 'Standard Scaler (Z-Score)',
            'description': 'Normalisasi dengan mean=0 dan std=1. Bagus untuk Linear Regression dan algoritma berbasis distance.',
            'formula': 'X_scaled = (X - mean) / std',
            'best_for': ['Linear Regression', 'Logistic Regression', 'SVM', 'Neural Networks']
        },
        'minmax': {
            'name': 'Min-Max Scaler',
            'description': 'Normalisasi ke range [0, 1]. Bagus jika ingin semua fitur dalam range yang sama.',
            'formula': 'X_scaled = (X - X_min) / (X_max - X_min)',
            'best_for': ['Neural Networks', 'Image Processing']
        },
        'robust': {
            'name': 'Robust Scaler',
            'description': 'Normalisasi menggunakan median dan IQR. Tahan terhadap outlier.',
            'formula': 'X_scaled = (X - median) / IQR',
            'best_for': ['Data with outliers', 'Linear Regression']
        }
    }
    
    return descriptions.get(scaler_type, descriptions['none'])