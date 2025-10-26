import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.dummy import DummyRegressor
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.preprocessing import MinMaxScaler
from xgboost import XGBRegressor
from catboost import CatBoostRegressor
from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout
from keras.callbacks import EarlyStopping
from utils.model_persistence import ModelPersistence

class ModelTrainer:
    """Class untuk melatih dan mengevaluasi Model Machine Learning"""
    
    def __init__(self):
        self.model = None
        self.model_name = None
        self.persistence = ModelPersistence(base_dir="saved_models")
        
    def get_model(self, model_name, params):
        """Initialize model based on name and parameters Inisialisasi model berdasarkan """
        if model_name == "Linear Regression":
            return LinearRegression(**params)
        elif model_name == "Decision Tree":
            return DecisionTreeRegressor(**params)
        elif model_name == "Random Forest":
            return RandomForestRegressor(**params)
        elif model_name == "Dummy Regressor":
            return DummyRegressor(**params)
        elif model_name == "XGBoost":
            return XGBRegressor(**params)
        elif model_name == "CatBoost":
            return CatBoostRegressor(verbose=0, **params)
        elif model_name == "SVR":
            return SVR(**params)
        elif model_name == "LSTM":
            return "LSTM"
        else:
            raise ValueError(f"Unknown model: {model_name}")
    
    def train_model(self, X_train, y_train, model_name, params):
        """Train the selected model"""
        self.model_name = model_name
        model = self.get_model(model_name, params)
        
        if model_name == "LSTM":
            # Normalisasi data
            scaler_X = MinMaxScaler()
            scaler_y = MinMaxScaler()
            X_scaled = scaler_X.fit_transform(X_train)
            y_scaled = scaler_y.fit_transform(y_train.values.reshape(-1, 1))
            
            # Bentuk urutan (sequence)
            window_size = params.get("window_size", 10)
            X_seq, y_seq = self.create_sequences(X_scaled, y_scaled, window_size)

            # Validasi panjang data
            if len(X_seq) == 0 or len(X_seq) != len(y_seq):
                raise ValueError(f"Invalid sequence shapes: X_seq={X_seq.shape}, y_seq={y_seq.shape}")
            
            n_features = X_seq.shape[2]
            
            # Definisi model LSTM
            lstm_model = Sequential([
                LSTM(64, return_sequences=True, input_shape=(window_size, n_features)),
                Dropout(0.2),
                LSTM(32, return_sequences=False),
                Dense(16, activation='relu'),
                Dense(1)
            ])
            
            lstm_model.compile(optimizer='adam', loss='mse')
            early_stop = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)
            
            lstm_model.fit(
                X_seq, y_seq,
                epochs=params.get("epochs", 100),
                batch_size=params.get("batch_size", 32),
                validation_split=0.2,
                verbose=0,
                callbacks=[early_stop]
            )
            
            self.model = lstm_model
            self.scaler_X = scaler_X
            self.scaler_y = scaler_y
            self.window_size = window_size
            
        else:
            # Untuk model biasa (sklearn)
            if len(X_train) != len(y_train):
                raise ValueError(f"Inconsistent training data sizes: X={len(X_train)}, y={len(y_train)}")
            self.model = model
            self.model.fit(X_train, y_train)
        
        return self.model

    def create_sequences(self, X, y, window_size):
        """Membuat urutan data time series"""
        Xs, ys = [], []
        for i in range(window_size, len(X)):
            Xs.append(X[i-window_size:i])
            ys.append(y[i])
        return np.array(Xs), np.array(ys)
    
    def evaluate_model(self, X_test, y_test):
        """Evaluate model performance"""
        if self.model is None:
            raise ValueError("Model has not been trained yet!")
        
        if self.model_name == "LSTM":
            X_scaled = self.scaler_X.transform(X_test)
            y_scaled = self.scaler_y.transform(y_test.values.reshape(-1, 1))
            
            X_seq, y_seq = self.create_sequences(X_scaled, y_scaled, self.window_size)
            if len(X_seq) == 0:
                raise ValueError("X_test too small for given window_size.")
            
            y_pred_scaled = self.model.predict(X_seq).flatten()
            y_pred = self.scaler_y.inverse_transform(y_pred_scaled.reshape(-1, 1)).flatten()
            y_true = self.scaler_y.inverse_transform(y_seq)
        else:
            y_pred = self.model.predict(X_test)
            y_true = y_test
        
        mae = mean_absolute_error(y_true, y_pred)
        mse = mean_squared_error(y_true, y_pred)
        rmse = np.sqrt(mse)
        mape = np.mean(np.abs((y_true - y_pred) / y_true)) * 100
        r2 = r2_score(y_true, y_pred)
        
        metrics = {
            "MAE": mae,
            "MSE": mse,
            "RMSE": rmse,
            "MAPE": mape,
            "R2": r2
        }
        
        return metrics, y_pred
    
    def get_feature_importance(self, feature_names):
        """Get feature importance or coefficients"""
        if self.model is None:
            raise ValueError("Model has not been trained yet!")

        if self.model_name == "LSTM":
            return None
        elif hasattr(self.model, 'coef_'):
            imp = dict(zip(feature_names, self.model.coef_))
        elif hasattr(self.model, 'feature_importances_'):
            imp = dict(zip(feature_names, self.model.feature_importances_))
        else:
            return None

        # Konversi ke tipe data aman JSON
        clean_imp = {}
        for k, v in imp.items():
            try:
                clean_imp[k] = float(v)
            except (ValueError, TypeError):
                clean_imp[k] = None
        return clean_imp
    
    def train_and_save(self, X_train, y_train, X_test, y_test, 
                       model_name, params, save_name=None, feature_names=None):
        """Train model, evaluate, dan simpan ke disk"""
        try:
            self.train_model(X_train, y_train, model_name, params)
            metrics, y_pred = self.evaluate_model(X_test, y_test)
            
            if feature_names is None:
                if hasattr(X_train, 'columns'):
                    feature_names = X_train.columns.tolist()
                else:
                    feature_names = [f"feature_{i}" for i in range(X_train.shape[1])]
            
            feature_importance = self.get_feature_importance(feature_names)
            
            from datetime import datetime
            if save_name is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                save_name = f"{model_name}_{timestamp}"
            
            model_data = {
                'model': self.model,
                'metrics': metrics,
                'params': params,
                'predictions': {
                    'y_pred': y_pred,
                    'y_test': y_test,
                    'feature_importance': feature_importance or {}
                }
            }
            
            success, message = self.persistence.save_model(save_name, model_data)
            
            return {
                'success': True,
                'model_name': save_name,
                'metrics': metrics,
                'y_pred': y_pred,
                'feature_importance': feature_importance,
                'save_status': success,
                'save_message': message
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def load_saved_model(self, model_name):
        """Load model dari disk"""
        model_data = self.persistence.load_model(model_name)
        if model_data:
            self.model = model_data['model']
            self.model_name = model_name
            return model_data
        return None
    
    def list_saved_models(self):
        """Dapatkan list semua model yang tersimpan"""
        return self.persistence.list_saved_models()
    
    def delete_saved_model(self, model_name):
        """Hapus model dari disk"""
        return self.persistence.delete_model(model_name)
    
    def get_storage_info(self):
        """Dapatkan informasi storage"""
        return self.persistence.get_storage_info()


def prepare_batch_data(data, batch_size=48):
    """
    Menggunakan feature engineering dari 48 baris untuk prediksi TARGET di baris ke-48.
    Ekstrak fitur statistik yang merepresentasikan pola temporal dari setiap kolom.
    
    Args:
        data: DataFrame dengan 16 kolom fitur + 1 kolom TARGET
        batch_size: Ukuran batch (default 48)
    
    Returns:
        X: DataFrame dengan fitur statistik
        y: Series dengan target values
        selected_features: List nama fitur yang digunakan
    """
    batches = []
    targets = []

    if 'Date' in data.columns:
        data = data.drop(columns=['Date'])

    if 'LIST_NUMBER' in data.columns:
        data = data.drop(columns=['LIST_NUMBER'])
    
    num_batches = len(data) // batch_size
    
    # Kolom fitur (semua kecuali TARGET)
    feature_cols = [col for col in data.columns if col != 'TARGET']
    
    for i in range(num_batches):
        batch = data.iloc[i * batch_size:(i + 1) * batch_size]
        
        # Gunakan SEMUA 48 baris untuk ekstrak fitur
        all_rows = batch.iloc[:]  # Semua 48 baris
        target_value = batch.iloc[-1]['TARGET']  # Target di baris ke-48
        
        # Dictionary untuk menyimpan fitur
        feature_dict = {}
        
        # Ekstrak fitur statistik untuk setiap kolom
        for col in feature_cols:
            col_data = all_rows[col]
            
            # Fitur statistik dasar
            feature_dict[f'{col}_mean'] = col_data.mean()
            feature_dict[f'{col}_std'] = col_data.std()
            feature_dict[f'{col}_min'] = col_data.min()
            feature_dict[f'{col}_max'] = col_data.max()
            feature_dict[f'{col}_median'] = col_data.median()
            
            # Fitur posisi (awal, tengah, akhir)
            feature_dict[f'{col}_first'] = col_data.iloc[0]
            feature_dict[f'{col}_mid'] = col_data.iloc[24]  # Tengah batch
            feature_dict[f'{col}_last'] = col_data.iloc[-1]
            
            # Fitur trend dan perubahan
            feature_dict[f'{col}_trend'] = col_data.iloc[-1] - col_data.iloc[0]
            feature_dict[f'{col}_range'] = col_data.max() - col_data.min()
            
            # Fitur kuartil
            feature_dict[f'{col}_q25'] = col_data.quantile(0.25)
            feature_dict[f'{col}_q75'] = col_data.quantile(0.75)
            
            # Fitur variasi temporal (perubahan per segment)
            segment1 = col_data.iloc[:16].mean()  # Segment 1-16
            segment2 = col_data.iloc[16:32].mean()  # Segment 17-32
            segment3 = col_data.iloc[32:].mean()  # Segment 33-48
            
            feature_dict[f'{col}_seg1'] = segment1
            feature_dict[f'{col}_seg2'] = segment2
            feature_dict[f'{col}_seg3'] = segment3
            feature_dict[f'{col}_seg_trend1'] = segment2 - segment1
            feature_dict[f'{col}_seg_trend2'] = segment3 - segment2
        
        batches.append(feature_dict)
        targets.append(target_value)
    
    X = pd.DataFrame(batches)
    y = pd.Series(targets, name='TARGET')
    
    return X, y, list(X.columns)

def split_data(X, y, test_size=0.2, random_state=42):
    """Split data into train and test sets"""
    return train_test_split(X, y, test_size=test_size, random_state=random_state)
