import streamlit as st
import pandas as pd

def show():
    """Display Saved Models Management page"""
    st.title("💾 Saved Models Management")
    st.markdown("Kelola model yang tersimpan di disk.")
    
    persistence = st.session_state.model_persistence
    
    # Storage info
    st.markdown("### 📊 Storage Information")
    storage_info = persistence.get_storage_info()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class='metric-card' style='text-align: center;'>
            <div class='metric-label'>Total Models</div>
            <div class='metric-value'>{storage_info['model_count']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class='metric-card' style='text-align: center;'>
            <div class='metric-label'>Storage Used</div>
            <div class='metric-value'>{storage_info['total_size_mb']} MB</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class='metric-card' style='text-align: center;'>
            <div class='metric-label'>Location</div>
            <div class='metric-value' style='font-size: 16px;'>{storage_info['base_dir']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # List saved models
    st.markdown("### 📂 Saved Models")
    
    saved_models = persistence.list_saved_models()
    
    if not saved_models:
        st.info("📭 Tidak ada model yang tersimpan. Train model terlebih dahulu di halaman **Model**.")
        return
    
    # Create dataframe
    models_df = pd.DataFrame(saved_models)
    models_df['MAE'] = models_df['metrics'].apply(lambda x: x['MAE'])
    models_df['RMSE'] = models_df['metrics'].apply(lambda x: x['RMSE'])
    models_df['R2'] = models_df['metrics'].apply(lambda x: x['R2'])
    
    display_df = models_df[['name', 'saved_at', 'MAE', 'RMSE', 'R2']]
    display_df.columns = ['Model Name', 'Saved At', 'MAE', 'RMSE', 'R² Score']
    
    st.dataframe(display_df, use_container_width=True)
    
    st.markdown("---")
    
    # Actions
    st.markdown("### ⚙️ Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔄 Reload All Models", use_container_width=True, type="primary"):
            with st.spinner("Memuat models dari disk..."):
                loaded, total = persistence.load_all_models()
                st.success(f"✅ {loaded}/{total} model(s) berhasil dimuat!")
                st.rerun()
    
    with col2:
        if st.button("🗑️ Clear Memory Only", use_container_width=True):
            st.session_state.trained_models = {}
            st.success("✅ Models cleared from memory (still saved on disk)")
            st.rerun()
    
    with col3:
        if st.button("💣 Delete All from Disk", use_container_width=True):
            if st.session_state.get("confirm_delete", False):
                # Confirm and delete
                st.session_state.trained_models = {}
                success, message = persistence.clear_all_saved_models()
                if success:
                    st.success(message)
                else:
                    st.error(message)
                st.session_state.confirm_delete = False
                st.rerun()
            else:
                st.session_state.confirm_delete = True
                st.warning("⚠️ Click again to confirm deletion!")
                st.rerun()
    
    st.markdown("---")
    
    # Individual model management
    st.markdown("### Individual Model Management")
    
    selected_model = st.selectbox(
        "Pilih model untuk kelola:",
        [m['name'] for m in saved_models]
    )
    
    if selected_model:
        model_info = next((m for m in saved_models if m['name'] == selected_model), None)
        
        if model_info:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### Model Details")
                st.write(f"**Name:** {model_info['name']}")
                st.write(f"**Saved At:** {model_info['saved_at']}")
                st.write(f"**MAE:** {model_info['metrics']['MAE']:.4f}")
                st.write(f"**RMSE:** {model_info['metrics']['RMSE']:.4f}")
                st.write(f"**R² Score:** {model_info['metrics']['R2']:.4f}")
            
            with col2:
                st.markdown("#### ⚙️ Actions")
                
                # Check if loaded
                is_loaded = selected_model in st.session_state.trained_models
                
                if is_loaded:
                    st.success("✅ Model loaded in memory")
                else:
                    if st.button("📥 Load to Memory", key=f"load_{selected_model}"):
                        model_data = persistence.load_model(selected_model)
                        if model_data:
                            st.session_state.trained_models[selected_model] = model_data
                            st.success(f"✅ Model '{selected_model}' loaded!")
                            st.rerun()
                        else:
                            st.error("❌ Failed to load model")
                
                st.markdown("---")
                
                if st.button("🗑️ Delete from Disk", key=f"delete_{selected_model}", type="secondary"):
                    # Delete from session if loaded
                    if selected_model in st.session_state.trained_models:
                        del st.session_state.trained_models[selected_model]
                    
                    # Delete from disk
                    success, message = persistence.delete_model(selected_model)
                    if success:
                        st.success(message)
                    else:
                        st.error(message)
                    st.rerun()
    
    st.markdown("---")
    
    # Tips
    st.markdown("### 💡 Tips")
    
    st.info("""
    **Model Persistence Features:**
    
    - ✅ **Auto-save**: Model otomatis tersimpan ke disk setelah training
    - 🔄 **Auto-load**: Saat restart aplikasi, model otomatis dimuat
    - 💾 **Persistent Storage**: Model tersimpan di folder `saved_models/`
    - 🗑️ **Individual Delete**: Hapus model tertentu tanpa menghapus semua
    - 📊 **Metadata**: Metrics dan parameters tersimpan bersama model
    
    **Storage Location:** `{storage_info['base_dir']}/`
    """)
    
    with st.expander("⚠️ Important Notes"):
        st.markdown("""
        1. Model disimpan menggunakan `pickle` format
        2. Pastikan tidak menghapus folder `saved_models/` secara manual
        3. Model yang tersimpan akan tetap ada meskipun streamlit di-restart
        4. Jika mengupdate kode model trainer, model lama mungkin tidak kompatibel
        5. Backup folder `saved_models/` secara berkala untuk keamanan data
        """)