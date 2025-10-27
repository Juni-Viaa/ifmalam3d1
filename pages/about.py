import streamlit as st

def show():
    """Display About page"""
    st.title("ℹ️ Tentang Aplikasi")
    
    # Header with styling
    st.markdown("""
    <div style='background: linear-gradient(135deg, #A7F3D0 0%, #6EE7B7 100%); 
                padding: 2rem; 
                border-radius: 12px; 
                text-align: center;
                margin-bottom: 2rem;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);'>
        <h2 style='color: #374151; margin: 0;'>ML Dashboard</h2>
        <p style='color: #374151; font-size: 18px; margin: 0.5rem 0 0 0;'>Machine Learning Model Training & Analysis Platform</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Version and basic info
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class='metric-card' style='text-align: center;'>
            <h3>📦 Version</h3>
            <p style='font-size: 24px; font-weight: bold;'>1.0.0</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='metric-card' style='text-align: center;'>
            <h3>🤖 Models</h3>
            <p style='font-size: 24px; font-weight: bold;'>3+</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class='metric-card' style='text-align: center;'>
            <h3>📊 Features</h3>
            <p style='font-size: 24px; font-weight: bold;'>16</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Description
    st.markdown("### 📖 Deskripsi")
    st.markdown("""
    Aplikasi **ML Dashboard** adalah platform analisis data menggunakan berbagai model Machine Learning.
    Aplikasi ini dirancang untuk menganalisis batch data dan memprediksi nilai TARGET berdasarkan 
    rata-rata fitur dari setiap batch (48 baris data).
    
    Platform ini memungkinkan Anda untuk:
    - Melatih multiple model ML dengan parameter yang dapat disesuaikan
    - Membandingkan performa antar model
    - Visualisasi hasil prediksi dengan berbagai grafik
    - Menganalisis kontribusi setiap fitur terhadap prediksi
    """)
    
    # Main Features
    st.markdown("---")
    st.markdown("### ✨ Fitur Utama")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        #### 📂 Data Management
        - Upload file Excel (.xlsx)
        - Automatic batch processing (48 rows per batch)
        - Feature averaging per batch
        - Data preview and validation
        
        #### 🤖 Machine Learning Models
        - **Linear Regression**: Simple, fast, interpretable
        - **Decision Tree**: Non-linear, easy to understand
        - **Random Forest**: Ensemble method, high accuracy
        - Customizable parameters for each model
        
        #### 📊 Visualization
        - Line charts for predictions
        - Scatter plots (Actual vs Predicted)
        - Residuals analysis
        - Feature importance/coefficients visualization
        """)
    
    with col2:
        st.markdown("""
        #### 📈 Model Evaluation
        - **MAE** (Mean Absolute Error)
        - **MSE** (Mean Squared Error)
        - **RMSE** (Root Mean Squared Error)
        - **MAPE** (Mean Absolute Percentage Error)
        - **R² Score** (Coefficient of Determination)
        
        #### ⚖️ Model Comparison
        - Side-by-side metrics comparison
        - Visual comparison with charts
        - Radar chart for normalized metrics
        - Best model recommendations
        
        #### 💾 Export Options
        - Download predictions as CSV
        - Export comparison tables
        - Save analysis results
        """)

    # Process Flow
    st.markdown("---")
    st.markdown("### 🔄 Alur Proses Analisis")
    
    st.markdown("""
    ```
    1. 📂 Upload Excel File
       ↓
    2. 🔄 Data Preprocessing
       • Group data into batches (48 rows each)
       • Calculate mean of each feature per batch
       • Extract target value from last row of each batch
       ↓
    3. ✂️ Train-Test Split
       • Default: 80% train, 20% test
       • Customizable split ratio
       ↓
    4. 🤖 Model Training
       • Select model type
       • Configure parameters
       • Train on training data
       ↓
    5. 📊 Model Evaluation
       • Calculate metrics (MAE, RMSE, R², etc.)
       • Generate predictions on test data
       ↓
    6. 📈 Visualization & Analysis
       • View prediction charts
       • Analyze feature importance
       • Compare with other models
    ```
    """)
    
    # Technology Stack
    st.markdown("---")
    st.markdown("### 🛠️ Teknologi yang Digunakan")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Frontend & Framework:**
        - **Streamlit**: Web application framework
        - **Custom CSS**: Tailwind-inspired styling
        - **Google Fonts**: Poppins & Roboto
        
        **Data Processing:**
        - **Pandas**: Data manipulation and analysis
        - **NumPy**: Numerical computations
        - **OpenPyXL**: Excel file handling
        """)
    
    with col2:
        st.markdown("""
        **Machine Learning:**
        - **Scikit-learn**: ML algorithms and metrics
        - **LinearRegression**: Linear modeling
        - **DecisionTreeRegressor**: Tree-based modeling
        - **RandomForestRegressor**: Ensemble modeling
        
        **Visualization:**
        - **Matplotlib**: Static plots and charts
        - **Custom color schemes**: Brand-consistent visuals
        """)
    
    # Tips & Best Practices
    st.markdown("---")
    st.markdown("### 💡 Tips & Best Practices")
    
    st.info("""
    **Untuk Hasil Terbaik:**
    
    1. **Data Quality**: Pastikan data clean dan tidak ada missing values
    2. **Batch Size**: Default 48 rows per batch - sesuaikan jika diperlukan
    3. **Model Selection**: 
       - Mulai dengan Linear Regression untuk baseline
       - Coba Decision Tree jika data non-linear
       - Gunakan Random Forest untuk akurasi maksimal
    4. **Parameter Tuning**: Eksperimen dengan berbagai parameter untuk hasil optimal
    5. **Cross-Validation**: Bandingkan multiple model untuk memilih yang terbaik
    6. **Feature Analysis**: Perhatikan feature importance untuk insight lebih dalam
    """)
    
    # Model Comparison Guide
    st.markdown("---")
    st.markdown("### 📊 Panduan Pemilihan Model")
    
    comparison_data = {
        "Aspect": ["Speed", "Accuracy", "Interpretability", "Complexity", "Overfitting Risk"],
        "Linear Regression": ["⚡⚡⚡", "⭐⭐", "⚡⚡⚡", "Low", "Low"],
        "Decision Tree": ["⚡⚡", "⭐⭐⭐", "⚡⚡⚡", "Medium", "High"],
        "Random Forest": ["⚡", "⭐⭐⭐⭐", "⭐", "High", "Low"]
    }
    
    import pandas as pd
    comparison_df = pd.DataFrame(comparison_data)
    st.dataframe(comparison_df, use_container_width=True)
    
    st.caption("⚡ = Speed | ⭐ = Rating")
    
    # FAQs
    st.markdown("---")
    st.markdown("### ❓ Frequently Asked Questions")
    
    with st.expander("Q: Berapa minimum data yang dibutuhkan?"):
        st.write("""
        Minimum 96 baris (2 batches) untuk dapat melakukan train-test split. 
        Namun, disarankan memiliki minimal 480 baris (10 batches) untuk hasil yang lebih reliable.
        """)
    
    with st.expander("Q: Apakah bisa menggunakan model lain selain yang tersedia?"):
        st.write("""
        Saat ini mendukung Linear Regression, Decision Tree, dan Random Forest. 
        Model tambahan dapat ditambahkan dengan mengupdate kode di `ml/model_trainer.py`.
        """)
    
    with st.expander("Q: Bagaimana cara memilih parameter terbaik?"):
        st.write("""
        Eksperimen dengan berbagai kombinasi parameter dan bandingkan metrik evaluasinya. 
        Gunakan halaman Perbandingan untuk melihat model mana yang memberikan hasil terbaik.
        """)
    
    with st.expander("Q: Apakah data saya aman?"):
        st.write("""
        Semua data diproses secara lokal di session Anda dan tidak disimpan ke server. 
        Data akan hilang ketika Anda menutup atau refresh aplikasi.
        """)
    
    # Contact & Support
    st.markdown("---")
    st.markdown("### 📞 Kontak & Dukungan")
    
    st.markdown("""
    <div style='background: #F3F4F6; padding: 1.5rem; border-radius: 8px; border-left: 4px solid #10B981;'>
        <p style='margin: 0;'><b>Butuh bantuan?</b></p>
        <p style='margin: 0.5rem 0 0 0;'>Silakan hubungi tim pengembang untuk pertanyaan, feedback, atau request fitur baru.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #6B7280; padding: 2rem 0;'>
        <p>Made with ❤️ using Streamlit</p>
        <p style='font-size: 14px;'>© 2024 ML Dashboard. All rights reserved.</p>
    </div>
    """, unsafe_allow_html=True)