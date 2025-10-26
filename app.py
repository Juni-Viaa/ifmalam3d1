import streamlit as st
from styles.custom_css import get_custom_css
from utils.session_manager import init_session_state
from utils.model_persistence import ModelPersistence
from pages import home, model, analysis, comparison, about, saved_models

# Konfigurasi halaman
st.set_page_config(
    page_title="ML Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
st.markdown(get_custom_css(), unsafe_allow_html=True)

# Initialize session state
init_session_state()

# Initialize model persistence
if "model_persistence" not in st.session_state:
    st.session_state.model_persistence = ModelPersistence()

# Auto-load saved models on first run
if "models_loaded" not in st.session_state:
    with st.spinner("Memuat saved models..."):
        loaded, total = st.session_state.model_persistence.load_all_models()
        if loaded > 0:
            st.success(f"✅ {loaded} model(s) berhasil dimuat dari disk!")
        st.session_state.models_loaded = True

# Sidebar - Model Selection
with st.sidebar:
    st.header("🤖 Model Machine Learning")
    st.markdown("---")

    ml_model = st.selectbox(
        "Pilih Model ML:",
        [
            "Dummy Regressor",
            "Linear Regression",
            "Decision Tree",
            "Random Forest",
            "XGBoost",
            "CatBoost",
            "SVR",
            "LSTM"
        ],
        key="ml_model_select"
    )

    st.session_state.selected_ml_model = ml_model

    st.markdown("---")
    st.subheader("📊 Deskripsi Model")

    descriptions = {
        "Dummy Regressor": "Model baseline sederhana yang hanya memprediksi rata-rata, median, atau nilai konstan dari target.",
        "Linear Regression": "Model regresi linear yang memprediksi nilai kontinu berdasarkan hubungan linear antar variabel.",
        "Decision Tree": "Model berbasis pohon keputusan yang memecah data berdasarkan fitur paling informatif.",
        "Random Forest": "Ensemble method yang menggabungkan banyak decision tree untuk akurasi lebih tinggi.",
        "XGBoost": "Gradient boosting algorithm yang sangat efisien dan sering digunakan untuk kompetisi ML.",
        "CatBoost": "Model boosting yang dioptimalkan untuk menangani data kategorikal dan mencegah overfitting.",
        "SVR": "Support Vector Regression menggunakan kernel untuk menemukan hubungan non-linear antara fitur dan target.",
        "LSTM": "Model deep learning berbasis jaringan saraf berulang (RNN) yang efektif mempelajari pola data berurutan/time-series."
    }

    st.info(descriptions[ml_model])

    st.markdown("---")
    st.subheader("⚙️ Parameter Model")

    # =========================
    # PARAMETER MODEL SECTION
    # =========================
    if ml_model == "Dummy Regressor":
        strategy = st.selectbox(
            "Strategi Prediksi",
            ["mean", "median", "constant"],
            key="dummy_strategy"
        )
        params = {"strategy": strategy}
        if strategy == "constant":
            const_value = st.number_input("Nilai Konstan", value=0.0, key="dummy_constant")
            params["constant"] = const_value
        st.session_state.model_params = params

    elif ml_model == "Linear Regression":
        st.session_state.model_params = {
            "fit_intercept": st.checkbox("Fit Intercept", value=True),
        }

    elif ml_model == "Decision Tree":
        max_depth = st.slider("Max Depth", 1, 20, 5, key="dt_max_depth")
        min_samples_split = st.slider("Min Samples Split", 2, 20, 2, key="dt_min_samples")
        st.session_state.model_params = {
            "max_depth": max_depth,
            "min_samples_split": min_samples_split,
            "random_state": 42
        }

    elif ml_model == "Random Forest":
        n_estimators = st.slider("N Estimators", 10, 300, 100, key="rf_n_estimators")
        max_depth = st.slider("Max Depth", 1, 30, 10, key="rf_max_depth")
        st.session_state.model_params = {
            "n_estimators": n_estimators,
            "max_depth": max_depth,
            "random_state": 42
        }

    elif ml_model == "XGBoost":
        n_estimators = st.slider("N Estimators", 50, 500, 100, key="xgb_n_estimators")
        learning_rate = st.slider("Learning Rate", 0.01, 0.5, 0.1, key="xgb_lr")
        max_depth = st.slider("Max Depth", 1, 15, 6, key="xgb_depth")
        st.session_state.model_params = {
            "n_estimators": n_estimators,
            "learning_rate": learning_rate,
            "max_depth": max_depth,
            "random_state": 42
        }

    elif ml_model == "CatBoost":
        n_estimators = st.slider("N Estimators", 50, 500, 200, key="cb_n_estimators")
        depth = st.slider("Depth", 2, 10, 6, key="cb_depth")
        learning_rate = st.slider("Learning Rate", 0.01, 0.3, 0.1, key="cb_lr")
        st.session_state.model_params = {
            "iterations": n_estimators,
            "depth": depth,
            "learning_rate": learning_rate,
            "random_seed": 42
        }

    elif ml_model == "SVR":
        kernel = st.selectbox("Kernel", ["linear", "poly", "rbf", "sigmoid"], key="svr_kernel")
        C = st.slider("C (Regularization)", 0.1, 10.0, 1.0, key="svr_C")
        epsilon = st.slider("Epsilon", 0.0, 1.0, 0.1, key="svr_epsilon")
        st.session_state.model_params = {
            "kernel": kernel,
            "C": C,
            "epsilon": epsilon
        }

    elif ml_model == "LSTM":
        epochs = st.slider("Epochs", 10, 300, 100, key="lstm_epochs")
        batch_size = st.slider("Batch Size", 8, 128, 32, key="lstm_batch")
        st.session_state.model_params = {
            "epochs": epochs,
            "batch_size": batch_size
        }

    st.markdown("---")
    st.caption("📌 Model yang dipilih: **" + ml_model + "**")

# ==========================================================
# Navigation Bar
# ==========================================================
def nav_button(label, page_name, icon, col):
    with col:
        is_active = st.session_state.page == page_name
        button_type = "primary" if is_active else "secondary"
        if st.button(f"{icon} {label}", key=f"btn_{page_name.lower()}", use_container_width=True, type=button_type):
            st.session_state.page = page_name
            st.rerun()

col1, col2, col3, col4, col5, col6 = st.columns(6)

nav_button("Home", "Home", "🏠", col1)
nav_button("Model", "Model", "📊", col2)
nav_button("Analisis", "Analisis", "📈", col3)
nav_button("Perbandingan", "Perbandingan", "⚖️", col4)
nav_button("Saved Models", "Saved Models", "💾", col5)
nav_button("Tentang", "Tentang", "ℹ️", col6)

st.divider()

# Route ke halaman yang sesuai
if st.session_state.page == "Home":
    home.show()
elif st.session_state.page == "Model":
    model.show()
elif st.session_state.page == "Analisis":
    analysis.show()
elif st.session_state.page == "Perbandingan":
    comparison.show()
elif st.session_state.page == "Saved Models":
    saved_models.show()
elif st.session_state.page == "Tentang":
    about.show()
