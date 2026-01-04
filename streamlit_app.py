import streamlit as st
import joblib
import os
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.datasets import load_iris
from sklearn.decomposition import PCA

# Page configuration
st.set_page_config(
    page_title="Iris Flower Predictor",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for premium look
st.markdown("""
<style>
    .main {
        background-color: #0e1117;
    }
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    }
    h1, h2, h3 {
        color: #00d2ff;
    }
    .stButton>button {
        background: linear-gradient(90deg, #00d2ff 0%, #3a7bd5 100%);
        color: white;
        border-radius: 10px;
        border: none;
        padding: 0.5rem 2rem;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 0 15px rgba(0, 210, 255, 0.4);
    }
    .prediction-card {
        background: rgba(255, 255, 255, 0.05);
        padding: 2rem;
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
    }
</style>
""", unsafe_allow_html=True)

# Load the trained model and target names
MODEL_PATH = 'model.joblib'
TARGET_NAMES_PATH = 'target_names.joblib'

@st.cache_resource
def load_model():
    if os.path.exists(MODEL_PATH) and os.path.exists(TARGET_NAMES_PATH):
        model = joblib.load(MODEL_PATH)
        target_names = joblib.load(TARGET_NAMES_PATH)
        return model, target_names
    return None, None

model, target_names = load_model()

@st.cache_data
def get_iris_data():
    iris = load_iris()
    return iris.data, iris.target, iris.target_names, iris.feature_names

X, y, names, feature_names = get_iris_data()

# Flower info
FLOWER_INFO = {
    'setosa': {
        'emoji': '🌸', 'color': '#FF6B9D',
        'description': 'Iris Setosa - Known for its small, delicate petals.',
        'facts': ['Smallest species', 'Native to Arctic', 'Blooms late spring']
    },
    'versicolor': {
        'emoji': '🌺', 'color': '#9B59B6',
        'description': 'Iris Versicolor - Also called the "Blue Flag".',
        'facts': ['Medium-sized', 'Found in wetlands', 'State flower of MI']
    },
    'virginica': {
        'emoji': '🌷', 'color': '#3498DB',
        'description': 'Iris Virginica - The largest species.',
        'facts': ['Largest iris', 'Native to NA', 'Grows up to 3ft']
    }
}

# Sidebar
with st.sidebar:
    st.title("Settings ⚙️")
    st.write("Adjust features to predict flower type.")
    
    sepal_l = st.slider("Sepal Length (cm)", 4.0, 8.0, 5.8, 0.1)
    sepal_w = st.slider("Sepal Width (cm)", 2.0, 4.5, 3.0, 0.1)
    petal_l = st.slider("Petal Length (cm)", 1.0, 7.0, 3.7, 0.1)
    petal_w = st.slider("Petal Width (cm)", 0.1, 2.5, 1.2, 0.1)
    
    predict_btn = st.button("Predict Species")

# Main Page
st.title("🌸 Iris Flower Predictor")
st.write("A premium machine learning app to classify Iris species.")

if predict_btn and model:
    input_data = np.array([[sepal_l, sepal_w, petal_l, petal_w]])
    prediction_idx = model.predict(input_data)[0]
    probs = model.predict_proba(input_data)[0]
    
    flower_name = target_names[prediction_idx]
    info = FLOWER_INFO.get(flower_name, {})
    confidence = probs[prediction_idx] * 100
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown(f"""
        <div class="prediction-card">
            <h2 style='color: {info.get('color', '#fff')}'>{info.get('emoji', '🌼')} {flower_name.capitalize()}</h2>
            <p><b>Confidence:</b> {confidence:.1f}%</p>
            <p>{info.get('description', '')}</p>
            <ul>
                {"".join([f"<li>{f}</li>" for f in info.get('facts', [])])}
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.write("### Prediction Probabilities")
        for i, name in enumerate(target_names):
            st.write(f"**{name.capitalize()}**")
            st.progress(float(probs[i]))
            st.write(f"{probs[i]*100:.1f}%")

# Visualization Tabs
tab1, tab2, tab3 = st.tabs(["📊 2D Analysis", "🌐 3D View", "✨ PCA Analysis"])

with tab1:
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    fig.patch.set_facecolor('#0e1117')
    
    # Sepal
    ax1 = axes[0]
    ax1.set_facecolor('#16162a')
    for i, name in enumerate(names):
        mask = y == i
        ax1.scatter(X[mask, 0], X[mask, 1], label=name.capitalize(), alpha=0.7)
    ax1.scatter(sepal_l, sepal_w, c='red', s=200, marker='*', label='You')
    ax1.set_xlabel('Sepal Length', color='white')
    ax1.set_ylabel('Sepal Width', color='white')
    ax1.tick_params(colors='white')
    ax1.legend()
    
    # Petal
    ax2 = axes[1]
    ax2.set_facecolor('#16162a')
    for i, name in enumerate(names):
        mask = y == i
        ax2.scatter(X[mask, 2], X[mask, 3], label=name.capitalize(), alpha=0.7)
    ax2.scatter(petal_l, petal_w, c='red', s=200, marker='*', label='You')
    ax2.set_xlabel('Petal Length', color='white')
    ax2.set_ylabel('Petal Width', color='white')
    ax2.tick_params(colors='white')
    ax2.legend()
    
    st.pyplot(fig)

with tab2:
    fig = plt.figure(figsize=(10, 8))
    fig.patch.set_facecolor('#0e1117')
    ax = fig.add_subplot(111, projection='3d')
    ax.set_facecolor('#16162a')
    
    for i, name in enumerate(names):
        mask = y == i
        ax.scatter(X[mask, 0], X[mask, 1], X[mask, 2], label=name.capitalize(), alpha=0.6)
    
    if predict_btn:
        ax.scatter(sepal_l, sepal_w, petal_l, c='red', s=300, marker='*', label='Current Prediction')
    
    ax.set_xlabel('Sepal L', color='white')
    ax.set_ylabel('Sepal W', color='white')
    ax.set_zlabel('Petal L', color='white')
    ax.tick_params(colors='white')
    st.pyplot(fig)

with tab3:
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor('#0e1117')
    ax.set_facecolor('#16162a')
    
    for i, name in enumerate(names):
        mask = y == i
        ax.scatter(X_pca[mask, 0], X_pca[mask, 1], label=name.capitalize(), alpha=0.7)
    
    ax.set_xlabel('Principal Component 1', color='white')
    ax.set_ylabel('Principal Component 2', color='white')
    ax.tick_params(colors='white')
    ax.legend()
    st.pyplot(fig)

if not model:
    st.error("Model files not found. Please ensure model.joblib and target_names.joblib are in the repository.")
