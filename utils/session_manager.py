import streamlit as st

def init_session_state():
    """Initialize all session state variables"""
    
    # Navigation
    if "page" not in st.session_state:
        st.session_state.page = "Home"
    
    # Model selection
    if "selected_ml_model" not in st.session_state:
        st.session_state.selected_ml_model = "Linear Regression"
    
    # Model parameters
    if "model_params" not in st.session_state:
        st.session_state.model_params = {}
    
    # Trained models storage
    if "trained_models" not in st.session_state:
        st.session_state.trained_models = {}
    
    # Data storage
    if "raw_data" not in st.session_state:
        st.session_state.raw_data = None
    
    if "X_train" not in st.session_state:
        st.session_state.X_train = None
    
    if "X_test" not in st.session_state:
        st.session_state.X_test = None
    
    if "y_train" not in st.session_state:
        st.session_state.y_train = None
    
    if "y_test" not in st.session_state:
        st.session_state.y_test = None
    
    if "selected_features" not in st.session_state:
        st.session_state.selected_features = []

def save_model_results(model_name, model, metrics, predictions):
    """Save trained model and its results to session state"""
    st.session_state.trained_models[model_name] = {
        "model": model,
        "metrics": metrics,
        "predictions": predictions,
        "params": st.session_state.model_params.copy()
    }

def get_model_results(model_name):
    """Retrieve model results from session state"""
    return st.session_state.trained_models.get(model_name, None)

def clear_all_models():
    """Clear all trained models"""
    st.session_state.trained_models = {}

def get_all_trained_models():
    """Get list of all trained model names"""
    return list(st.session_state.trained_models.keys())