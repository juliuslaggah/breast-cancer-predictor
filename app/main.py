import streamlit as st
import pickle
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from utils import login_user, logout_user
from pathlib import Path
from dicom import load_dicom_series, segment_volume, plot_slice_mask, compute_mask_features




# ------------------- CONSTANTS ------------------- #
SLIDER_LABELS = [
    ("Radius (mean)", "radius_mean"),
    ("Texture (mean)", "texture_mean"),
    ("Perimeter (mean)", "perimeter_mean"),
    ("Area (mean)", "area_mean"),
    ("Smoothness (mean)", "smoothness_mean"),
    ("Compactness (mean)", "compactness_mean"),
    ("Concavity (mean)", "concavity_mean"),
    ("Concave points (mean)", "concave points_mean"),
    ("Symmetry (mean)", "symmetry_mean"),
    ("Fractal dimension (mean)", "fractal_dimension_mean"),
    ("Radius (se)", "radius_se"),
    ("Texture (se)", "texture_se"),
    ("Perimeter (se)", "perimeter_se"),
    ("Area (se)", "area_se"),
    ("Smoothness (se)", "smoothness_se"),
    ("Compactness (se)", "compactness_se"),
    ("Concavity (se)", "concavity_se"),
    ("Concave points (se)", "concave points_se"),
    ("Symmetry (se)", "symmetry_se"),
    ("Fractal dimension (se)", "fractal_dimension_se"),
    ("Radius (worst)", "radius_worst"),
    ("Texture (worst)", "texture_worst"),
    ("Perimeter (worst)", "perimeter_worst"),
    ("Area (worst)", "area_worst"),
    ("Smoothness (worst)", "smoothness_worst"),
    ("Compactness (worst)", "compactness_worst"),
    ("Concavity (worst)", "concavity_worst"),
    ("Concave points (worst)", "concave points_worst"),
    ("Symmetry (worst)", "symmetry_worst"),
    ("Fractal dimension (worst)", "fractal_dimension_worst"),
]

# ------------------- CONFIGURATION ------------------- #
st.set_page_config(
    page_title="Breast Cancer Predictor",
    page_icon=":female-doctor:",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
css_file = Path(__file__).parent.parent / "assets/style.css"
with open("assets/style.css", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    
    
    

# ------------------- AUTHENTICATION ------------------- #
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
  col1, col2 = st.columns([1.8, 3], gap="large")
  with col1:
      login_success = login_user()
  with col2:
    st.markdown("### Welcome to our Breast Cancer prediction APP")
    logo_col, team_col = st.columns([5,3], gap="large")
    with logo_col:
        image_path = Path(__file__).parent.parent / "assets/logo.jpeg"
        st.image(image_path, use_container_width=1000)
        
    with team_col:
        st.markdown("""
         <div style='margin-top: 2rem;'>
            <h4 style='color: #01DB4B; border-bottom: 1px solid #415a77; padding-bottom: 0.5rem;'>
             Meet our Team
         </h4>
            <div style='break-inside: avoid;'>
                • Julius Laggah - Data Scientist<br>
                • Abdul Karim Jusu - Backend Dev<br>
                • Sandar Win - Frontend Dev<br>
                • Adamsay Turay - Frontend Dev
    </div>
    """, unsafe_allow_html=True)
        
    
    
    if not login_success:
        st.stop()
    
else:
    if st.sidebar.button("Logout"):
        logout_user()
        st.rerun()

# ------------------- CORE FUNCTIONS ------------------- #
def get_clean_data():
    data_file = Path(__file__).parent.parent / "data/data.csv"
    data = pd.read_csv(data_file)
    data = data.drop(['Unnamed: 32'], axis=1)
    data['diagnosis'] = data['diagnosis'].map({'M': 1, 'B': 0})
    return data


MEDICAL_PLAUSIBLE_RANGES = {
    # Mean Features
    'radius_mean': (0.00, 28.11),         
    'texture_mean': (0.00, 39.28),        
    'perimeter_mean': (0.00, 188.50),    
    'area_mean': (0.00, 2501.00),        
    'smoothness_mean': (0.00, 0.16),     
    'compactness_mean': (0.00, 0.35),     
    'concavity_mean': (0.00, 0.43),        
    'concave points_mean': (0.00, 0.20),   
    'symmetry_mean': (0.00, 0.30),         
    'fractal_dimension_mean': (0.00, 0.10), 

    # Standard Error Features
    'radius_se': (0.00, 2.87),
    'texture_se': (0.00, 4.88),
    'perimeter_se': (0.00, 21.98),
    'area_se': (0.00,542.20),
    'smoothness_se': (0.00, 0.03),
    'compactness_se': (0.00, 0.14),
    'concavity_se': (0.00, 0.40),
    'concave points_se': (0.00, 0.05),
    'symmetry_se': (0.00, 0.08),
    'fractal_dimension_se': (0.00, 0.03),

    # Worst Features
    'radius_worst': (0.00, 36.04),
    'texture_worst': (0.00, 49.54),
    'perimeter_worst': (0.00, 251.20),
    'area_worst': (0.00, 4254.00),
    'smoothness_worst': (0.00, 0.22),
    'compactness_worst': (0.00, 1.06),
    'concavity_worst': (0.00, 1.25),
    'concave points_worst': (0.00, 0.29),
    'symmetry_worst': (0.00, 0.66),
    'fractal_dimension_worst': (0.00, 0.21)
}




def add_sidebar():

    st.sidebar.header("Cell Nuclei Measurement")
    
    manual_mode = st.sidebar.checkbox(
        "🖥️ Switch to Manual Input", 
        key="manual_mode",
        help="Enter exact values instead of using sliders"
    )
    
    data = get_clean_data()
    input_dict = {}

    for label, key in SLIDER_LABELS:
        med_min, med_max = MEDICAL_PLAUSIBLE_RANGES.get(key, (0.00, float('inf')))
        
        
        
        if manual_mode:
            # Number inputs for manual mode
            input_dict[key]= st.sidebar.number_input(
                label,
                min_value=0.0,
                max_value=float(data[key].max()),
                value=float(data[key].mean()),
                step=0.01,
                format="%.2f",
                key=f"manual_{key}"
            )
            
            if input_dict[key] < med_min:
                st.sidebar.error(f"❌ Below typical minimum ({med_min})")
            elif input_dict[key] > med_max:
                st.sidebar.error(f"❌ Exceeds clinical maximum ({med_max})")
                
                
                
                
        else:
            # Original sliders
            input_dict[key] = st.sidebar.slider(
                label,
                min_value=float(0),
                max_value=float(data[key].max()),
                value=float(data[key].mean()),
                key=f"slider_{key}"
            )
    # Add separator
    st.sidebar.markdown("---")
    # DICOM CONTROLS
    st.sidebar.header("📂 DICOM Image Segmentation")
    dicom_folder = st.sidebar.text_input("🔍 Folder path to DICOMs", "")
    segment_method = st.sidebar.selectbox("Segmentation method", ["otsu"], index=0)
    slice_idx = st.sidebar.number_input("🧠 Slice index", min_value=0, value=0, step=1)
    

    return input_dict, dicom_folder, segment_method, slice_idx



def get_scaled_values(input_dict):
    data = get_clean_data()
    X = data.drop(['diagnosis'], axis=1)
    scaled_dict = {}
    
    for key, value in input_dict.items():
        max_val = X[key].max()
        min_val = X[key].min()
        scaled_value = (value - min_val) / (max_val - min_val)
        scaled_dict[key] = scaled_value
    
    return scaled_dict

def get_radar_chart(input_data):
    input_data = get_scaled_values(input_data)
    categories = ['Radius', 'Texture', 'Perimeter', 'Area',
                'Smoothness', 'Compactness', 'Concavity',
                'Concave Points', 'Symmetry', 'Fractal Dimension']

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=[
            input_data['radius_mean'],
            input_data['texture_mean'],
            input_data['perimeter_mean'],
            input_data['area_mean'],
            input_data['smoothness_mean'],
            input_data['compactness_mean'],
            input_data['concavity_mean'],
            input_data['concave points_mean'],
            input_data['symmetry_mean'],
            input_data['fractal_dimension_mean']
        ],
        theta=categories,
        fill='toself',
        name='Mean'
    ))
    
    fig.add_trace(go.Scatterpolar(
        r=[
            input_data['radius_se'],
            input_data['texture_se'],
            input_data['perimeter_se'],
            input_data['area_se'],
            input_data['smoothness_se'],
            input_data['compactness_se'],
            input_data['concavity_se'],
            input_data['concave points_se'],
            input_data['symmetry_se'],
            input_data['fractal_dimension_se']
        ],
        theta=categories,
        fill='toself',
        name='Standard Error'
    ))

    fig.add_trace(go.Scatterpolar(
        r=[
            input_data['radius_worst'],
            input_data['texture_worst'],
            input_data['perimeter_worst'],
            input_data['area_worst'],
            input_data['smoothness_worst'],
            input_data['compactness_worst'],
            input_data['concavity_worst'],
            input_data['concave points_worst'],
            input_data['symmetry_worst'],
            input_data['fractal_dimension_worst']
        ],
        theta=categories,
        fill='toself',
        name='Worst'
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1]
            )
        ),
        showlegend=True,
        height=600
    )
    
    return fig

def add_predictions(input_data, imaging_features: dict = None):
    
    if imaging_features is None:
        model_path = Path(__file__).parent.parent / "model/model_v3.pkl"
        scaler_path = Path(__file__).parent.parent / "model/scaler_v3.pkl"
        
        feats = input_data.copy()
        
    else:
        model_path = Path(__file__).parent.parent / "model/model_v2.pkl"
        scaler_path = Path(__file__).parent.parent / "model/scaler_v2.pkl"
        
        feats = {**input_data, **imaging_features}

    
    model = pickle.load(open(model_path, "rb"))
    scaler = pickle.load(open(scaler_path, "rb"))
    
    vals = [feats[k] for (_, k) in SLIDER_LABELS]
    if imaging_features is not None:
        vals += [
            feats["volume_cm3"],
            feats["mean_area_px"],
            feats["surface_area_cm2"],
        ]
    
    

    input_array = np.array(vals).reshape(1, -1)
    input_array_scaled = scaler.transform(input_array)

    prediction = model.predict(input_array_scaled)
    probabilities = model.predict_proba(input_array_scaled)[0]

    st.subheader("Cell Cluster Prediction")
    st.write("The cell cluster is:")
    
    if prediction[0] == 0:
        st.markdown("<div class='diagnosis benign'>Benign</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='diagnosis malicious'>Malignant</div>", unsafe_allow_html=True)
        
        
        st.markdown("""
            <div class='clinical-guidelines'>
             <h4 class='guideline-header'>Clinical Protocol Recommendations</h4>
             <div class='guideline-content'>
            """, unsafe_allow_html=True)

    if prediction[0] == 1:  # Malignant
        st.markdown("""
    <div class='critical-guidelines'>
        <h5>NCCN Guidelines (Category 4B+)</h5>
        <ul>
            <li>🩺 Core needle biopsy required</li>
            <li>📸 Diagnostic mammography + ultrasound</li>
            <li>🧪 Estrogen receptor testing</li>
            <li>⚕️ Surgical oncology consultation</li>
            <li>⏳ Treatment within 14 days</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    else:  # Benign
        st.markdown("""
    <div class='routine-guidelines'>
        <h5>Follow-up Protocol (BI-RADS 3)</h5>
        <ul>
            <li>📅 6-month follow-up ultrasound</li>
            <li>🔄 Comparative imaging analysis</li>
            <li>📝 Patient self-examination education</li>
            <li>⚖️ Risk factor modification counseling</li>
            <li>🚨 Report new symptoms immediately</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

        st.markdown("</div></div>", unsafe_allow_html=True)
        
        
        
        

    st.metric("Benign Probability", f"{probabilities[0]:.2%}")
    st.metric("Malignant Probability", f"{probabilities[1]:.2%}")
    
    st.caption("This tool assists medical professionals but should not replace professional diagnosis.")
    
    
    
    
    

def batch_prediction_section():
    st.divider()
    st.subheader("Batch Predictions from CSV")
    
    uploaded_file = st.file_uploader(
        "Upload breast cytology data CSV",
        type=["csv"],
        accept_multiple_files=False
    )

    if not uploaded_file:
        return 
    try:
            # Read and clean data first
        batch_data = pd.read_csv(uploaded_file)
            
            
            # Drop unnecessary columns if they exist
        batch_data = batch_data.drop(columns=['id, Unnamed: 32'], errors='ignore')
            
            # Get required features from slider labels
        required_cols = [key for (label, key) in SLIDER_LABELS]
            
            # Validate columns
        missing_cols = set(required_cols) - set(batch_data.columns)
        if missing_cols:
            st.error(f"Missing required columns: {', '.join(missing_cols)}")
            return

            # Load model and scaler
        model_path = Path(__file__).parent.parent / "model/model_v3.pkl"
        scaler_path = Path(__file__).parent.parent / "model/scaler_v3.pkl"
            
        model = pickle.load(open(model_path, "rb"))
        scaler = pickle.load(open(scaler_path, "rb"))

            # Scale the data using the same scaler
        scaled_data = scaler.transform(batch_data[required_cols])
            
            # Make predictions
        predictions = model.predict(scaled_data)
        probabilities = model.predict_proba(scaled_data)

            # Create clean results dataframe
        results = batch_data[required_cols].copy()
        results['Prediction'] = ['Benign' if p == 0 else 'Malignant' for p in predictions]
        results['Benign Probability'] = probabilities[:, 0]
        results['Malignant Probability'] = probabilities[:, 1]

            # Format and display results
        st.dataframe(results.style.format({
                'Benign Probability': '{:.2%}',
                'Malignant Probability': '{:.2%}'
            }))

            # Create clean download CSV
        csv = results.to_csv(index=False).encode('utf-8')
        st.download_button(
                "Download Predictions",
                data=csv,
                file_name="cancer_predictions.csv",
                mime="text/csv"
            )

    except Exception as e:
        st.error(f"Error processing file: {str(e)}")
            
# ------------------- MAIN APP ------------------- #
def main():
    if not st.session_state.authenticated:
        return

    input_data, dicom_folder, segment_method, slice_idx = add_sidebar()


    # Main content container
    with st.container():
        st.title("Breast Cancer Diagnosis Predictor")
        st.write("""
        Clinical decision support tool for breast mass cytology analysis. 
        Adjust measurements using the sidebar sliders to get real-time predictions.
        """)
        
        
    
    
    

    # Columns layout
    col1, col2 = st.columns([4, 1], gap="large")
    
    with col1:
        st.header("Measurement Radar Chart")
        fig = get_radar_chart(input_data)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        add_predictions(input_data)
    
    # Batch predictions section
    batch_prediction_section()
    
    
    
    # ✅ DICOM Image Visualization Section
    if dicom_folder:
        st.subheader("DICOM Image Segmentation Viewer")

        try:
            volume = load_dicom_series(dicom_folder)
            mask = segment_volume(volume, method=segment_method)
            fig = plot_slice_mask(volume, mask, slice_index=slice_idx)
            st.pyplot(fig)
            
            
            img_feats = compute_mask_features(volume, mask, voxel_spacing=(1, 1, 1))
            with st.expander("🧮 Imaging Quantitative Features"):
                st.metric("Volume (cm³)",    f"{img_feats['volume_cm3']:.2f}")
                st.metric("Mean Area (px)",  f"{img_feats['mean_area_px']:.2f}")
                st.metric("Surface Area (cm²)", f"{img_feats['surface_area_cm2']:.2f}")
                
                st.markdown("---")
                st.markdown("## Combined Cytology + Imaging Prediction")
                add_predictions(input_data, imaging_features=img_feats)
            
        except Exception as e:
            st.error(f"❌ Error processing DICOM: {e}")
    
    
    

if __name__ == "__main__":
    main()