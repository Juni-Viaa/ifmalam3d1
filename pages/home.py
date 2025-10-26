import streamlit as st

def show():
    """Display Home page"""
    st.title("Dashboard Machine Learning")
    st.markdown(
        "<p style='font-size:18px; color:#6B7280;'>Visualisasi dan analisis model Machine Learning berdasarkan rata-rata fitur setiap batch (48 baris).</p>",
        unsafe_allow_html=True
    )

    # Welcome Section
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### Selamat Datang!

        Aplikasi ini dirancang untuk membantu Anda:
        
        -**Upload Data**: Mengunggah file Excel dengan data batch
        -**Train Model**: Melatih berbagai model Machine Learning
        -**Visualisasi**: Melihat hasil prediksi dalam bentuk grafik
        -**Analisis**: Menganalisis kontribusi setiap fitur
        -**Perbandingan**: Membandingkan performa antar model
        
        Silakan upload file Excel Anda di halaman **Model** untuk memulai analisis.
        """)
    
    with col2:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #A7F3D0 0%, #6EE7B7 100%); 
                    padding: 2rem; 
                    border-radius: 12px; 
                    text-align: center;
                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);'>
            <h2 style='color: #374151; margin: 0;'>🚀</h2>
            <h3 style='color: #374151; margin: 10px 0;'>Mulai Sekarang</h3>
            <p style='color: #374151; font-size: 14px;'>Upload data Anda dan mulai analisis ML</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Features Grid
    st.markdown("### Fitur Utama")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class='metric-card'>
            <h3>📊 Multi-Model Support</h3>
            <p>Mendukung Linear Regression, Decision Tree, dan Random Forest dengan parameter yang dapat disesuaikan.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='metric-card'>
            <h3>📈 Evaluasi Lengkap</h3>
            <p>Metrik evaluasi komprehensif: MAE, MSE, RMSE, MAPE, dan R² Score untuk setiap model.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class='metric-card'>
            <h3>⚖️ Model Comparison</h3>
            <p>Bandingkan performa berbagai model secara side-by-side untuk memilih model terbaik.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Quick Tips
    st.markdown("### 💡 Tips Penggunaan")
    
    st.info("""
    **Langkah-langkah:**
    1. Pastikan file Excel Anda sudah sesuai format
    2. Pilih model ML di sidebar
    3. Atur parameter model sesuai kebutuhan
    4. Upload file di halaman **Model**
    5. Lihat hasil analisis di halaman **Analisis**
    6. Bandingkan model di halaman **Perbandingan**
    """)

    # Status Check
    st.markdown("---")
    st.markdown("### Status Sistem")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.session_state.get("raw_data") is not None:
            st.success("✅ Data Loaded")
        else:
            st.warning("⏳ No Data")
    
    with col2:
        trained_count = len(st.session_state.get("trained_models", {}))
        if trained_count > 0:
            st.success(f"✅ {trained_count} Model(s) Trained")
        else:
            st.warning("⏳ No Models")
    
    with col3:
        current_model = st.session_state.get("selected_ml_model", "None")
        st.info(f"🤖 Current: {current_model}")