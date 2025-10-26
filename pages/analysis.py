import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def show():
    """Display Analysis page"""
    st.title("Analisis Model")
    
    # Check if models are trained
    trained_models = st.session_state.get("trained_models", {})
    
    if not trained_models:
        st.warning("⚠️ Belum ada model yang dilatih. Silakan latih model terlebih dahulu di halaman **Model**!")
        return
    
    # Model selection
    st.markdown("### Pilih Model untuk Analisis")
    model_names = list(trained_models.keys())
    
    selected_model = st.selectbox(
        "Pilih Model:",
        model_names,
        key="analysis_model_select"
    )
    
    if selected_model:
        model_data = trained_models[selected_model]
        metrics = model_data["metrics"]
        predictions = model_data["predictions"]
        y_pred = predictions["y_pred"]
        y_test = predictions["y_test"]
        feature_importance = predictions.get("feature_importance", None)
        
        st.info(f"Menganalisis model: **{selected_model}**")
        
        # Display metrics summary
        st.markdown("---")
        st.markdown("### Ringkasan Metrik Evaluasi")
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.markdown(f"""
            <div class='metric-card' style='text-align: center;'>
                <div class='metric-label'>MAE</div>
                <div class='metric-value'>{metrics['MAE']:.4f}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class='metric-card' style='text-align: center;'>
                <div class='metric-label'>MSE</div>
                <div class='metric-value'>{metrics['MSE']:.4f}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class='metric-card' style='text-align: center;'>
                <div class='metric-label'>RMSE</div>
                <div class='metric-value'>{metrics['RMSE']:.4f}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class='metric-card' style='text-align: center;'>
                <div class='metric-label'>MAPE</div>
                <div class='metric-value'>{metrics['MAPE']:.2f}%</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col5:
            st.markdown(f"""
            <div class='metric-card' style='text-align: center;'>
                <div class='metric-label'>R² Score</div>
                <div class='metric-value'>{metrics['R2']:.4f}</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Visualization section
        st.markdown("---")
        st.markdown("### Visualisasi Prediksi vs Aktual")
        
        # Create comparison dataframe
        comparison_df = pd.DataFrame({
            "Index": range(len(y_test)),
            "Nilai Aktual": y_test if isinstance(y_test, np.ndarray) else y_test.values,
            "Nilai Prediksi": y_pred
        }).reset_index(drop=True)
        
        # Number of data points to display
        col1, col2 = st.columns([3, 1])
        with col2:
            n_points = st.slider("Jumlah Data", 10, min(200, len(comparison_df)), min(100, len(comparison_df)))
        
        comparison_display = comparison_df.head(n_points)
        
        # Line chart
        st.markdown("#### Diagram Garis")
        fig, ax = plt.subplots(figsize=(14, 6))
        ax.plot(comparison_display["Index"], comparison_display["Nilai Aktual"], 
                label="Nilai Aktual", marker='o', color='#10B981', linewidth=2.5, markersize=4)
        ax.plot(comparison_display["Index"], comparison_display["Nilai Prediksi"], 
                label="Nilai Prediksi", marker='x', color='#3B82F6', linewidth=2.5, markersize=4)
        ax.set_title(f"Perbandingan Nilai Aktual vs Prediksi - {selected_model}", 
                    fontsize=16, fontweight='600', fontfamily='Poppins')
        ax.set_xlabel("Data ke-", fontsize=14, fontfamily='Roboto')
        ax.set_ylabel("Nilai TARGET", fontsize=14, fontfamily='Roboto')
        ax.legend(fontsize=12, loc='best')
        ax.grid(True, linestyle='--', alpha=0.3)
        plt.tight_layout()
        st.pyplot(fig)
        
        # Scatter plot
        st.markdown("#### Scatter Plot - Actual vs Predicted")
        fig, ax = plt.subplots(figsize=(10, 8))
        ax.scatter(comparison_display["Nilai Aktual"], comparison_display["Nilai Prediksi"], 
                  alpha=0.6, s=50, color='#A7F3D0', edgecolors='#10B981', linewidth=1.5)
        
        # Perfect prediction line
        min_val = min(comparison_display["Nilai Aktual"].min(), comparison_display["Nilai Prediksi"].min())
        max_val = max(comparison_display["Nilai Aktual"].max(), comparison_display["Nilai Prediksi"].max())
        ax.plot([min_val, max_val], [min_val, max_val], 'r--', linewidth=2, label='Perfect Prediction')
        
        ax.set_xlabel("Nilai Aktual", fontsize=14, fontfamily='Roboto')
        ax.set_ylabel("Nilai Prediksi", fontsize=14, fontfamily='Roboto')
        ax.set_title(f"Scatter Plot: Actual vs Predicted - {selected_model}", 
                    fontsize=16, fontweight='600', fontfamily='Poppins')
        ax.legend(fontsize=12)
        ax.grid(True, linestyle='--', alpha=0.3)
        plt.tight_layout()
        st.pyplot(fig)
        
        # Residuals plot
        st.markdown("#### Residuals Plot")
        residuals = comparison_display["Nilai Aktual"] - comparison_display["Nilai Prediksi"]
        
        fig, ax = plt.subplots(figsize=(14, 6))
        ax.scatter(comparison_display["Index"], residuals, alpha=0.6, s=50, 
                  color='#A7F3D0', edgecolors='#10B981', linewidth=1.5)
        ax.axhline(y=0, color='r', linestyle='--', linewidth=2)
        ax.set_xlabel("Data ke-", fontsize=14, fontfamily='Roboto')
        ax.set_ylabel("Residuals (Aktual - Prediksi)", fontsize=14, fontfamily='Roboto')
        ax.set_title(f"Residuals Plot - {selected_model}", 
                    fontsize=16, fontweight='600', fontfamily='Poppins')
        ax.grid(True, linestyle='--', alpha=0.3)
        plt.tight_layout()
        st.pyplot(fig)
        
        # Data table
        st.markdown("---")
        st.markdown("### Tabel Perbandingan Data")
        
        # Add error column
        comparison_display_with_error = comparison_display.copy()
        comparison_display_with_error["Error"] = comparison_display_with_error["Nilai Aktual"] - comparison_display_with_error["Nilai Prediksi"]
        comparison_display_with_error["Absolute Error"] = abs(comparison_display_with_error["Error"])
        
        st.dataframe(comparison_display_with_error, use_container_width=True)
        
        # Download option
        csv = comparison_display_with_error.to_csv(index=False)
        st.download_button(
            label="📥 Download Data as CSV",
            data=csv,
            file_name=f"predictions_{selected_model}.csv",
            mime="text/csv"
        )
        
        # Feature importance/coefficients
        if feature_importance:
            st.markdown("---")
            st.markdown("### Analisis Fitur")
            
            # Convert to dataframe and sort
            if selected_model == "Linear Regression":
                feature_label = "Koefisien"
                description = "Koefisien menunjukkan kontribusi setiap fitur terhadap prediksi. Nilai positif meningkatkan prediksi, nilai negatif menurunkannya."
            else:
                feature_label = "Importance"
                description = "Feature importance menunjukkan seberapa penting setiap fitur dalam membuat prediksi. Nilai lebih tinggi = lebih penting."
            
            st.info(description)
            
            feature_df = pd.DataFrame({
                "Fitur": list(feature_importance.keys()),
                feature_label: list(feature_importance.values())
            }).sort_values(by=feature_label, ascending=False)
            
            #Display table 
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.markdown(f"#### Tabel {feature_label}")
                st.dataframe(feature_df, use_container_width=True)
            
            with col2:
                st.markdown(f"#### Visualisasi {feature_label}")
                fig, ax = plt.subplots(figsize=(10, 8))
                
                if selected_model == "Linear Regression":
                    colors = ['#10B981' if x > 0 else '#EF4444' for x in feature_df[feature_label]]
                else:
                    colors = '#10B981'
                
                ax.barh(feature_df['Fitur'], feature_df[feature_label], color=colors, alpha=0.7)
                ax.set_xlabel(f'Nilai {feature_label}', fontsize=12, fontfamily='Roboto')
                ax.set_title(f'{feature_label} Fitur - {selected_model}', 
                           fontsize=14, fontweight='600', fontfamily='Poppins')
                ax.grid(True, linestyle='--', alpha=0.3, axis='x')
                plt.tight_layout()
                st.pyplot(fig)