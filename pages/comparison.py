import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def show():
    """Display Model Comparison page"""
    st.title("Perbandingan Model")
    st.markdown("Bandingkan performa berbagai model Machine Learning secara side-by-side.")
    
    # Check if models are trained
    trained_models = st.session_state.get("trained_models", {})
    
    if not trained_models:
        st.warning("⚠️ Belum ada model yang dilatih. Silakan latih minimal 1 model di halaman **Model**!")
        return
    
    if len(trained_models) < 2:
        st.info("💡 Anda telah melatih 1 model. Latih lebih banyak model untuk melihat perbandingan yang lebih lengkap!")
    
    # Show number of trained models
    st.success(f"✅ Total model yang telah dilatih: **{len(trained_models)}**")
    
    # Metrics comparison table
    st.markdown("---")
    st.markdown("### Perbandingan Metrik Evaluasi")
    
    # Prepare comparison dataframe
    comparison_data = []
    for model_name, model_data in trained_models.items():
        metrics = model_data["metrics"]
        comparison_data.append({
            "Model": model_name,
            "MAE": metrics["MAE"],
            "MSE": metrics["MSE"],
            "RMSE": metrics["RMSE"],
            "MAPE (%)": metrics["MAPE"],
            "R² Score": metrics["R2"]
        })
    
    comparison_df = pd.DataFrame(comparison_data)
    
    # Highlight best values
    st.dataframe(
        comparison_df.style.highlight_min(
            subset=["MAE", "MSE", "RMSE", "MAPE (%)"],
            color="#C6F6D5"
        ).highlight_max(
            subset=["R² Score"],
            color="#C6F6D5"
        ),
        use_container_width=True
    )
    
    st.caption("💡 Hijau menandakan nilai terbaik untuk setiap metrik")
    
    # Best model summary
    st.markdown("---")
    st.markdown("### Ringkasan Model Terbaik")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        best_mae_idx = comparison_df["MAE"].idxmin()
        best_mae_model = comparison_df.loc[best_mae_idx, "Model"]
        best_mae_value = comparison_df.loc[best_mae_idx, "MAE"]
        st.markdown(f"""
        <div class='metric-card' style='text-align: center;'>
            <h4 style='color: #10B981;'>Lowest MAE</h4>
            <h3>{best_mae_model}</h3>
            <p style='font-size: 24px; font-weight: bold;'>{best_mae_value:.4f}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        best_rmse_idx = comparison_df["RMSE"].idxmin()
        best_rmse_model = comparison_df.loc[best_rmse_idx, "Model"]
        best_rmse_value = comparison_df.loc[best_rmse_idx, "RMSE"]
        st.markdown(f"""
        <div class='metric-card' style='text-align: center;'>
            <h4 style='color: #10B981;'>Lowest RMSE</h4>
            <h3>{best_rmse_model}</h3>
            <p style='font-size: 24px; font-weight: bold;'>{best_rmse_value:.4f}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        best_r2_idx = comparison_df["R² Score"].idxmax()
        best_r2_model = comparison_df.loc[best_r2_idx, "Model"]
        best_r2_value = comparison_df.loc[best_r2_idx, "R² Score"]
        st.markdown(f"""
        <div class='metric-card' style='text-align: center;'>
            <h4 style='color: #10B981;'>Highest R²</h4>
            <h3>{best_r2_model}</h3>
            <p style='font-size: 24px; font-weight: bold;'>{best_r2_value:.4f}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Visual comparison
    st.markdown("---")
    st.markdown("### Visualisasi Perbandingan")
    
    # Select metrics to compare
    col1, col2 = st.columns([3, 1])
    with col2:
        chart_type = st.radio("Chart Type:", ["Bar Chart", "Radar Chart"], key="chart_type")
    
    if chart_type == "Bar Chart":
        # Bar charts for each metric
        fig, axes = plt.subplots(2, 3, figsize=(18, 10))
        fig.suptitle("Perbandingan Metrik Antar Model", fontsize=18, fontweight='600', fontfamily='Poppins')
        
        metrics_to_plot = [
            ("MAE", False),
            ("MSE", False),
            ("RMSE", False),
            ("MAPE (%)", False),
            ("R² Score", True)
        ]
        
        for idx, (metric, higher_better) in enumerate(metrics_to_plot):
            row = idx // 3
            col = idx % 3
            ax = axes[row, col]
            
            values = comparison_df[metric]
            models = comparison_df["Model"]
            
            # Color: green for best, light green for others
            if higher_better:
                best_idx = values.idxmax()
            else:
                best_idx = values.idxmin()
            
            colors = ['#10B981' if i == best_idx else '#A7F3D0' for i in range(len(values))]
            
            bars = ax.bar(models, values, color=colors, alpha=0.8)
            ax.set_title(metric, fontsize=14, fontweight='600', fontfamily='Poppins')
            ax.set_ylabel("Value", fontsize=12, fontfamily='Roboto')
            ax.tick_params(axis='x', rotation=45)
            ax.grid(True, linestyle='--', alpha=0.3, axis='y')
            
            # Add value labels on bars
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{height:.4f}',
                       ha='center', va='bottom', fontsize=10)
        
        # Remove empty subplot
        fig.delaxes(axes[1, 2])
        
        plt.tight_layout()
        st.pyplot(fig)
    
    else:  # Radar Chart
        st.markdown("#### 🎯 Radar Chart - Normalized Metrics")
        
        # Normalize metrics (0-1 scale)
        normalized_df = comparison_df.copy()
        
        # For metrics where lower is better, invert the normalization
        for col in ["MAE", "MSE", "RMSE", "MAPE (%)"]:
            max_val = normalized_df[col].max()
            min_val = normalized_df[col].min()
            if max_val != min_val:
                # Invert: lower values get higher scores
                normalized_df[col] = 1 - (normalized_df[col] - min_val) / (max_val - min_val)
            else:
                normalized_df[col] = 0.5
        
        # For R² Score, higher is better (no inversion needed)
        max_val = normalized_df["R² Score"].max()
        min_val = normalized_df["R² Score"].min()
        if max_val != min_val:
            normalized_df["R² Score"] = (normalized_df["R² Score"] - min_val) / (max_val - min_val)
        else:
            normalized_df["R² Score"] = 0.5
        
        # Prepare data for radar chart
        categories = ["MAE", "MSE", "RMSE", "MAPE", "R²"]
        
        fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))
        
        angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
        angles += angles[:1]  # Complete the circle
        
        colors = ['#10B981', '#3B82F6', '#F59E0B', '#EF4444', '#8B5CF6']
        
        for idx, (_, row) in enumerate(normalized_df.iterrows()):
            values = [
                row["MAE"],
                row["MSE"],
                row["RMSE"],
                row["MAPE (%)"],
                row["R² Score"]
            ]
            values += values[:1]  # Complete the circle
            
            ax.plot(angles, values, 'o-', linewidth=2, label=row["Model"], 
                   color=colors[idx % len(colors)])
            ax.fill(angles, values, alpha=0.15, color=colors[idx % len(colors)])
        
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories, fontsize=12)
        ax.set_ylim(0, 1)
        ax.set_title("Normalized Metrics Comparison", fontsize=16, fontweight='600', 
                    fontfamily='Poppins', pad=20)
        ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1), fontsize=10)
        ax.grid(True, linestyle='--', alpha=0.3)
        
        plt.tight_layout()
        st.pyplot(fig)
        
        st.caption("💡 Semua metrik dinormalisasi ke skala 0-1, dimana nilai lebih tinggi = performa lebih baik")
    
    # Detailed comparison
    st.markdown("---")
    st.markdown("### Perbandingan Detail")
    
    # Select two models to compare
    if len(trained_models) >= 2:
        col1, col2 = st.columns(2)
        
        model_names = list(trained_models.keys())
        
        with col1:
            model1 = st.selectbox("Model 1:", model_names, key="compare_model1")
        
        with col2:
            model2 = st.selectbox("Model 2:", 
                                 [m for m in model_names if m != model1], 
                                 key="compare_model2")
        
        if model1 and model2:
            st.markdown(f"#### {model1} vs {model2}")
            
            model1_data = trained_models[model1]
            model2_data = trained_models[model2]
            
            # Side by side comparison
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"##### {model1}")
                metrics1 = model1_data["metrics"]
                st.markdown(f"""
                <div style='background: #F0FDF4; padding: 1.5rem; border-radius: 8px; border: 2px solid #A7F3D0;'>
                    <p><b>MAE:</b> {metrics1['MAE']:.4f}</p>
                    <p><b>MSE:</b> {metrics1['MSE']:.4f}</p>
                    <p><b>RMSE:</b> {metrics1['RMSE']:.4f}</p>
                    <p><b>MAPE:</b> {metrics1['MAPE']:.2f}%</p>
                    <p><b>R² Score:</b> {metrics1['R2']:.4f}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"##### {model2}")
                metrics2 = model2_data["metrics"]
                st.markdown(f"""
                <div style='background: #EFF6FF; padding: 1.5rem; border-radius: 8px; border: 2px solid #93C5FD;'>
                    <p><b>MAE:</b> {metrics2['MAE']:.4f}</p>
                    <p><b>MSE:</b> {metrics2['MSE']:.4f}</p>
                    <p><b>RMSE:</b> {metrics2['RMSE']:.4f}</p>
                    <p><b>MAPE:</b> {metrics2['MAPE']:.2f}%</p>
                    <p><b>R² Score:</b> {metrics2['R2']:.4f}</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Difference analysis
            st.markdown("##### Analisis Perbedaan")
            
            diff_mae = ((metrics1['MAE'] - metrics2['MAE']) / metrics2['MAE'] * 100)
            diff_rmse = ((metrics1['RMSE'] - metrics2['RMSE']) / metrics2['RMSE'] * 100)
            diff_r2 = ((metrics1['R2'] - metrics2['R2']) / abs(metrics2['R2']) * 100) if metrics2['R2'] != 0 else 0
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                color = "red" if diff_mae > 0 else "green"
                arrow = "↑" if diff_mae > 0 else "↓"
                st.markdown(f"""
                <div style='text-align: center; padding: 1rem; background: white; border-radius: 8px; border: 1px solid #E5E7EB;'>
                    <p style='color: #6B7280; margin: 0;'>MAE Difference</p>
                    <p style='color: {color}; font-size: 20px; font-weight: bold; margin: 0.5rem 0;'>
                        {arrow} {abs(diff_mae):.2f}%
                    </p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                color = "red" if diff_rmse > 0 else "green"
                arrow = "↑" if diff_rmse > 0 else "↓"
                st.markdown(f"""
                <div style='text-align: center; padding: 1rem; background: white; border-radius: 8px; border: 1px solid #E5E7EB;'>
                    <p style='color: #6B7280; margin: 0;'>RMSE Difference</p>
                    <p style='color: {color}; font-size: 20px; font-weight: bold; margin: 0.5rem 0;'>
                        {arrow} {abs(diff_rmse):.2f}%
                    </p>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                color = "green" if diff_r2 > 0 else "red"
                arrow = "↑" if diff_r2 > 0 else "↓"
                st.markdown(f"""
                <div style='text-align: center; padding: 1rem; background: white; border-radius: 8px; border: 1px solid #E5E7EB;'>
                    <p style='color: #6B7280; margin: 0;'>R² Difference</p>
                    <p style='color: {color}; font-size: 20px; font-weight: bold; margin: 0.5rem 0;'>
                        {arrow} {abs(diff_r2):.2f}%
                    </p>
                </div>
                """, unsafe_allow_html=True)
            
            st.caption(f"💡 Persentase relatif terhadap {model2}")
            
            # Predictions comparison
            st.markdown("---")
            st.markdown("##### Perbandingan Prediksi")
            
            pred1 = model1_data["predictions"]["y_pred"]
            pred2 = model2_data["predictions"]["y_pred"]
            y_test = model1_data["predictions"]["y_test"]
            
            # Take first 50 points for visualization
            n_points = min(50, len(pred1))
            
            fig, ax = plt.subplots(figsize=(14, 6))
            x_range = range(n_points)
            
            ax.plot(x_range, y_test[:n_points] if isinstance(y_test, np.ndarray) else y_test.values[:n_points], 
                   label="Actual", marker='o', color='#000000', linewidth=2.5, markersize=6)
            ax.plot(x_range, pred1[:n_points], 
                   label=model1, marker='s', color='#10B981', linewidth=2, markersize=5, alpha=0.7)
            ax.plot(x_range, pred2[:n_points], 
                   label=model2, marker='^', color='#3B82F6', linewidth=2, markersize=5, alpha=0.7)
            
            ax.set_title(f"Perbandingan Prediksi: {model1} vs {model2}", 
                        fontsize=16, fontweight='600', fontfamily='Poppins')
            ax.set_xlabel("Data ke-", fontsize=14, fontfamily='Roboto')
            ax.set_ylabel("Nilai TARGET", fontsize=14, fontfamily='Roboto')
            ax.legend(fontsize=12, loc='best')
            ax.grid(True, linestyle='--', alpha=0.3)
            plt.tight_layout()
            st.pyplot(fig)
    
    # Recommendations
    st.markdown("---")
    st.markdown("### 💡 Rekomendasi")
    
    # Find overall best model
    best_overall_idx = comparison_df["R² Score"].idxmax()
    best_overall_model = comparison_df.loc[best_overall_idx, "Model"]
    
    st.success(f"""
    **Model Terbaik Secara Keseluruhan: {best_overall_model}**
    
    Berdasarkan R² Score, model **{best_overall_model}** menunjukkan performa terbaik dalam menjelaskan variasi data.
    """)
    
    # Additional insights
    with st.expander("📋 Insight Tambahan", expanded=False):
        st.markdown("""
        **Tips Memilih Model:**
        
        1. **R² Score Tinggi (> 0.8)**: Model sangat baik dalam menjelaskan data
        2. **MAE/RMSE Rendah**: Model memiliki error prediksi yang kecil
        3. **MAPE Rendah**: Persentase error relatif terhadap nilai aktual kecil
        
        **Pertimbangan:**
        - Jika Anda membutuhkan **interpretabilitas**, pilih Linear Regression atau Decision Tree
        - Jika Anda membutuhkan **akurasi tinggi**, pilih Random Forest
        - Jika Anda membutuhkan **kecepatan training**, pilih Linear Regression
        
        **Model Complexity vs Performance:**
        - Linear Regression: Simple, fast, interpretable
        - Decision Tree: Moderate complexity, interpretable
        - Random Forest: High complexity, highest accuracy
        """)
    
    # Export comparison
    st.markdown("---")
    st.markdown("### 📥 Export Data")
    
    csv = comparison_df.to_csv(index=False)
    st.download_button(
        label="Download Comparison Table (CSV)",
        data=csv,
        file_name="model_comparison.csv",
        mime="text/csv"
    )