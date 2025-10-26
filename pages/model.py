import streamlit as st
import pandas as pd
from ml.model_trainer import ModelTrainer, prepare_batch_data, split_data
from utils.session_manager import save_model_results

def show():
    """Display Model Training page"""
    st.title("Train Model")
    st.markdown("Upload file Excel dan latih model Machine Learning pilihan Anda.")

    # Model info
    current_model = st.session_state.get("selected_ml_model", "Linear Regression")
    st.info(f"Model yang akan dilatih: **{current_model}**")

    # File uploader
    uploaded_file = st.file_uploader("📂 Upload file Excel", type=["xlsx"])

    if uploaded_file:
        try:
            # Load data
            data = pd.read_excel(uploaded_file)
            st.success(f"✅ Data berhasil diunggah! Jumlah baris: {len(data)}")
            
            # Save raw data
            st.session_state.raw_data = data

            # Show data preview
            with st.expander("Preview Data (48 baris pertama)", expanded=False):
                st.dataframe(data.head(48), use_container_width=True)

            st.markdown("---")

            # Prepare batch data
            st.markdown("### 🔄 Preprocessing Data")
            
            with st.spinner("Memproses data menjadi batch..."):
                X, y, selected_features = prepare_batch_data(data, batch_size=48)
                st.session_state.selected_features = selected_features
            
            st.success(f"✅ Data berhasil diproses menjadi {len(X)} batch!")

            # Split data
            st.markdown("---")
            st.markdown("### ✂️ Split Data")
            
            col1, col2 = st.columns(2)
            with col1:
                test_size = st.slider("Test Size (%)", 10, 40, 20, step=5)
            with col2:
                random_state = st.number_input("Random State", 0, 100, 42)
            
            X_train, X_test, y_train, y_test = split_data(
                X, y, 
                test_size=test_size/100, 
                random_state=random_state
            )
            
            # Save to session state
            st.session_state.X_train = X_train
            st.session_state.X_test = X_test
            st.session_state.y_train = y_train
            st.session_state.y_test = y_test
            
            st.info(f"Training set: {len(X_train)} samples | Test set: {len(X_test)} samples")

            # Train Model Section
            st.markdown("---")
            st.markdown("### Train Model")
            
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                st.markdown(f"**Model:** {current_model}")
                st.markdown(f"**Parameters:** {st.session_state.get('model_params', {})}")
            
            with col2:
                train_button = st.button("Train Model", type="primary", use_container_width=True)
            
            with col3:
                if st.button("🗑️ Clear All Models", use_container_width=True):
                    # Clear from session
                    st.session_state.trained_models = {}
                    # Clear from disk
                    if 'model_persistence' in st.session_state:
                        success, message = st.session_state.model_persistence.clear_all_saved_models()
                        if success:
                            st.success("✅ All models cleared from memory and disk!")
                        else:
                            st.error(message)
                    else:
                        st.warning("Model persistence not initialized")
                    st.rerun()

            # Training process
            if train_button:
                with st.spinner(f"Training {current_model}..."):
                    try:
                        # 🔴 PERBAIKAN 1: Gunakan trainer dari session_state atau buat baru
                        if 'trainer' not in st.session_state:
                            st.session_state.trainer = ModelTrainer()
                        
                        trainer = st.session_state.trainer
                        
                        # Get parameters
                        params = st.session_state.get("model_params", {})
                        
                        # 🔴 PERBAIKAN 2: Gunakan train_and_save() untuk auto-save
                        result = trainer.train_and_save(
                            X_train, y_train, X_test, y_test,
                            model_name=current_model,
                            params=params,
                            save_name=current_model,  # Nama untuk disimpan
                            feature_names=selected_features
                        )
                        
                        if result['success']:
                            # Extract data dari result
                            metrics = result['metrics']
                            y_pred = result['y_pred']
                            feature_importance = result['feature_importance']
                            
                            # Save to session state juga (untuk compatibility)
                            save_model_results(
                                current_model,
                                trainer.model,  # Model object
                                metrics,
                                {
                                    "y_pred": y_pred,
                                    "y_test": y_test,
                                    "feature_importance": feature_importance
                                }
                            )
                            
                            # Show save status
                            if result['save_status']:
                                st.success(f"✅ Model {current_model} berhasil dilatih dan disimpan ke disk!")
                                st.caption(result['save_message'])
                            else:
                                st.warning(f"⚠️ Model berhasil dilatih tapi gagal disimpan: {result['save_message']}")
                            
                            # Display metrics
                            st.markdown("---")
                            st.markdown("### 📈 Hasil Evaluasi Model")
                            
                            # Metrics in columns
                            col1, col2, col3, col4, col5 = st.columns(5)
                            
                            with col1:
                                st.metric("MAE", f"{metrics['MAE']:.4f}")
                            with col2:
                                st.metric("MSE", f"{metrics['MSE']:.4f}")
                            with col3:
                                st.metric("RMSE", f"{metrics['RMSE']:.4f}")
                            with col4:
                                st.metric("MAPE", f"{metrics['MAPE']:.2f}%")
                            with col5:
                                st.metric("R² Score", f"{metrics['R2']:.4f}")
                            
                            # Detailed metrics
                            with st.expander("📊 Detail Metrik Evaluasi", expanded=True):
                                st.markdown(f"""
                                <div style='background: #F0FDF4; padding: 1.5rem; border-radius: 8px; border: 2px solid #A7F3D0;'>
                                    <p><b>Mean Absolute Error (MAE):</b> {metrics['MAE']:.4f}</p>
                                    <p><b>Mean Squared Error (MSE):</b> {metrics['MSE']:.4f}</p>
                                    <p><b>Root Mean Squared Error (RMSE):</b> {metrics['RMSE']:.4f}</p>
                                    <p><b>Mean Absolute Percentage Error (MAPE):</b> {metrics['MAPE']:.2f}%</p>
                                    <p><b>R² Score:</b> {metrics['R2']:.4f}</p>
                                    <hr style='margin: 1rem 0; border-color: #A7F3D0;'>
                                    <p style='font-size: 14px; color: #6B7280;'><i>
                                    MAE mengukur rata-rata kesalahan absolut. Semakin kecil semakin baik.<br>
                                    R² Score mengukur seberapa baik model menjelaskan variasi data (0-1, semakin tinggi semakin baik).
                                    </i></p>
                                </div>
                                """, unsafe_allow_html=True)
                            
                            st.info("💡 Lihat visualisasi lengkap di halaman **Analisis** dan bandingkan dengan model lain di **Perbandingan**")
                        
                        else:
                            st.error(f"❌ Error saat training model: {result['error']}")
                        
                    except Exception as e:
                        st.error(f"❌ Error saat training model: {str(e)}")
                        import traceback
                        st.code(traceback.format_exc())

            # Show trained models
            st.markdown("---")
            st.markdown("### Model yang Telah Dilatih")
            
            # 🔴 PERBAIKAN 3: Show storage info dengan error handling
            if 'trainer' in st.session_state:
                try:
                    storage_info = st.session_state.trainer.get_storage_info()
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Total Models", storage_info['model_count'])
                    with col2:
                        st.metric("Storage Used", f"{storage_info['total_size_mb']} MB")
                    with col3:
                        st.metric("Location", storage_info['base_dir'])
                except Exception as e:
                    st.warning(f"Could not load storage info: {str(e)}")
            
            st.markdown("---")
            
            # 🔴 PERBAIKAN 4: Show both session state and disk models
            trained_models = st.session_state.get("trained_models", {})
            
            # Option to load models from disk
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown("#### Models in Memory")
            with col2:
                if st.button("📂 Load from Disk"):
                    if 'trainer' in st.session_state:
                        saved_models = st.session_state.trainer.list_saved_models()
                        for model_info in saved_models:
                            if model_info['name'] not in trained_models:
                                # Load model
                                loaded = st.session_state.trainer.load_saved_model(model_info['name'])
                                if loaded:
                                    # Add to session state
                                    st.session_state.trained_models[model_info['name']] = loaded
                        st.success("Models loaded from disk!")
                        st.rerun()
            
            if trained_models:
                for model_name, model_data in trained_models.items():
                    with st.expander(f"📊 {model_name}", expanded=False):
                        metrics = model_data["metrics"]
                        params = model_data["params"]
                        
                        col1, col2, col3 = st.columns([2, 2, 1])
                        
                        with col1:
                            st.markdown("**Metrics:**")
                            st.write(f"- MAE: {metrics['MAE']:.4f}")
                            st.write(f"- RMSE: {metrics['RMSE']:.4f}")
                            st.write(f"- R²: {metrics['R2']:.4f}")
                        
                        with col2:
                            st.markdown("**Parameters:**")
                            for param, value in params.items():
                                st.write(f"- {param}: {value}")
                        
                        with col3:
                            # Delete button
                            if st.button("🗑️ Delete", key=f"delete_{model_name}"):
                                # Remove from session
                                del st.session_state.trained_models[model_name]
                                # Remove from disk
                                if 'trainer' in st.session_state:
                                    success, msg = st.session_state.trainer.delete_saved_model(model_name)
                                    if success:
                                        st.success(msg)
                                    else:
                                        st.error(msg)
                                st.rerun()
            else:
                st.info("Belum ada model yang dilatih. Silakan train model terlebih dahulu.")
                
                # Check if there are models on disk
                if 'trainer' in st.session_state:
                    saved_models = st.session_state.trainer.list_saved_models()
                    if saved_models:
                        st.info(f"💡 Ada {len(saved_models)} model tersimpan di disk. Klik 'Load from Disk' untuk memuatnya.")

        except Exception as e:
            st.error(f"❌ Error saat memproses file: {str(e)}")
            st.info("Pastikan file Excel Anda memiliki format yang benar dengan kolom yang diperlukan.")
            
            # Show traceback for debugging
            with st.expander("🔍 Debug Info"):
                import traceback
                st.code(traceback.format_exc())

    else:
        st.warning("⚠️ Silakan upload file Excel terlebih dahulu!")
        
        # Show available models on disk (jika ada)
        if 'trainer' in st.session_state:
            st.markdown("---")
            st.markdown("### 💾 Models Available on Disk")
            
            saved_models = st.session_state.trainer.list_saved_models()
            
            if saved_models:
                st.info(f"Found {len(saved_models)} saved models")
                
                for model_info in saved_models:
                    with st.expander(f"📊 {model_info['name']}", expanded=False):
                        st.write(f"**Saved at:** {model_info['saved_at']}")
                        st.json(model_info['metrics'])
            else:
                st.info("No saved models found on disk yet.")