from flask import Flask, render_template, request, jsonify, send_file
import joblib
import os
import numpy as np
import io
import base64
from functools import lru_cache

# Import matplotlib with Agg backend for server-side rendering
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.datasets import load_iris
from sklearn.decomposition import PCA

app = Flask(__name__)

# Configuration for performance
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 31536000  # Cache static files for 1 year

# Load the trained model and target names
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model.joblib')
TARGET_NAMES_PATH = os.path.join(os.path.dirname(__file__), 'target_names.joblib')

# Cache the model loading
@lru_cache(maxsize=1)
def load_model():
    """Load the trained model from joblib file (cached for performance)."""
    try:
        model = joblib.load(MODEL_PATH)
        target_names = joblib.load(TARGET_NAMES_PATH)
        return model, target_names
    except FileNotFoundError:
        print("❌ Model not found! Please run train_model.py first.")
        return None, None

# Load model at startup
model, target_names = load_model()

# Cache the iris dataset
@lru_cache(maxsize=1)
def get_iris_data():
    """Load and cache the Iris dataset."""
    iris = load_iris()
    return iris.data, iris.target, iris.target_names, iris.feature_names

# Flower information for display
FLOWER_INFO = {
    'setosa': {
        'emoji': '🌸',
        'color': '#FF6B9D',
        'description': 'Iris Setosa - Known for its small, delicate petals and distinctive purple/blue coloring.',
        'facts': ['Smallest of the three species', 'Native to Arctic regions', 'Blooms in late spring']
    },
    'versicolor': {
        'emoji': '🌺',
        'color': '#9B59B6',
        'description': 'Iris Versicolor - Also called the "Blue Flag", features beautiful purple-blue flowers.',
        'facts': ['Medium-sized iris species', 'Found in wetlands', 'State flower of Michigan']
    },
    'virginica': {
        'emoji': '🌷',
        'color': '#3498DB',
        'description': 'Iris Virginica - The largest of the three species with striking violet-blue flowers.',
        'facts': ['Largest iris species', 'Native to eastern North America', 'Can grow up to 3 feet tall']
    }
}

@app.route('/')
def home():
    """Render the home page."""
    return render_template('index.html', prediction=None)

@app.route('/predict', methods=['POST'])
def predict():
    """Handle prediction request."""
    if model is None:
        return render_template('index.html', 
                               prediction=None, 
                               error="Model not loaded. Please train the model first!")
    
    try:
        # Get input values from form
        sepal_length = float(request.form['sepal_length'])
        sepal_width = float(request.form['sepal_width'])
        petal_length = float(request.form['petal_length'])
        petal_width = float(request.form['petal_width'])
        
        # Validate inputs
        features = [sepal_length, sepal_width, petal_length, petal_width]
        for val in features:
            if val <= 0:
                return render_template('index.html',
                                       prediction=None,
                                       error="All values must be positive numbers!")
        
        # Make prediction
        input_features = np.array([features])
        prediction_idx = model.predict(input_features)[0]
        prediction_proba = model.predict_proba(input_features)[0]
        
        # Get flower name and info
        flower_name = target_names[prediction_idx]
        flower_info = FLOWER_INFO.get(flower_name, {})
        confidence = prediction_proba[prediction_idx] * 100
        
        # Get all probabilities
        all_probs = {
            target_names[i].capitalize(): round(prediction_proba[i] * 100, 1)
            for i in range(len(target_names))
        }
        
        result = {
            'flower_name': flower_name.capitalize(),
            'emoji': flower_info.get('emoji', '🌼'),
            'color': flower_info.get('color', '#3498DB'),
            'description': flower_info.get('description', ''),
            'facts': flower_info.get('facts', []),
            'confidence': f"{confidence:.1f}%",
            'all_probabilities': all_probs,
            'input_values': {
                'sepal_length': sepal_length,
                'sepal_width': sepal_width,
                'petal_length': petal_length,
                'petal_width': petal_width
            }
        }
        
        return render_template('index.html', prediction=result)
        
    except ValueError:
        return render_template('index.html',
                               prediction=None,
                               error="Please enter valid numeric values!")
    except Exception as e:
        return render_template('index.html',
                               prediction=None,
                               error=f"An error occurred: {str(e)}")

@app.route('/chart/2d')
def chart_2d():
    """Generate 2D scatter plot of Iris dataset."""
    try:
        X, y, names, feature_names = get_iris_data()
        
        # Create figure with dark background support
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        fig.patch.set_facecolor('#1a1a2e')
        
        colors = ['#FF6B9D', '#9B59B6', '#3498DB']
        
        # Plot 1: Sepal Length vs Sepal Width
        ax1 = axes[0, 0]
        ax1.set_facecolor('#16162a')
        for i, (color, name) in enumerate(zip(colors, names)):
            mask = y == i
            ax1.scatter(X[mask, 0], X[mask, 1], c=color, label=name.capitalize(), 
                       alpha=0.7, edgecolors='white', s=60)
        ax1.set_xlabel('Sepal Length (cm)', color='white')
        ax1.set_ylabel('Sepal Width (cm)', color='white')
        ax1.set_title('Sepal Dimensions', color='white', fontsize=12, fontweight='bold')
        ax1.legend(facecolor='#1a1a2e', edgecolor='white', labelcolor='white')
        ax1.tick_params(colors='white')
        for spine in ax1.spines.values():
            spine.set_color('white')
        
        # Plot 2: Petal Length vs Petal Width
        ax2 = axes[0, 1]
        ax2.set_facecolor('#16162a')
        for i, (color, name) in enumerate(zip(colors, names)):
            mask = y == i
            ax2.scatter(X[mask, 2], X[mask, 3], c=color, label=name.capitalize(),
                       alpha=0.7, edgecolors='white', s=60)
        ax2.set_xlabel('Petal Length (cm)', color='white')
        ax2.set_ylabel('Petal Width (cm)', color='white')
        ax2.set_title('Petal Dimensions', color='white', fontsize=12, fontweight='bold')
        ax2.legend(facecolor='#1a1a2e', edgecolor='white', labelcolor='white')
        ax2.tick_params(colors='white')
        for spine in ax2.spines.values():
            spine.set_color('white')
        
        # Plot 3: Sepal Length vs Petal Length
        ax3 = axes[1, 0]
        ax3.set_facecolor('#16162a')
        for i, (color, name) in enumerate(zip(colors, names)):
            mask = y == i
            ax3.scatter(X[mask, 0], X[mask, 2], c=color, label=name.capitalize(),
                       alpha=0.7, edgecolors='white', s=60)
        ax3.set_xlabel('Sepal Length (cm)', color='white')
        ax3.set_ylabel('Petal Length (cm)', color='white')
        ax3.set_title('Sepal vs Petal Length', color='white', fontsize=12, fontweight='bold')
        ax3.legend(facecolor='#1a1a2e', edgecolor='white', labelcolor='white')
        ax3.tick_params(colors='white')
        for spine in ax3.spines.values():
            spine.set_color('white')
        
        # Plot 4: Feature Distribution (Box Plot)
        ax4 = axes[1, 1]
        ax4.set_facecolor('#16162a')
        bp = ax4.boxplot([X[:, i] for i in range(4)], patch_artist=True,
                        labels=['Sepal L', 'Sepal W', 'Petal L', 'Petal W'])
        for patch, color in zip(bp['boxes'], ['#FF6B9D', '#9B59B6', '#3498DB', '#2ecc71']):
            patch.set_facecolor(color)
            patch.set_alpha(0.7)
        for element in ['whiskers', 'fliers', 'means', 'medians', 'caps']:
            plt.setp(bp[element], color='white')
        ax4.set_title('Feature Distribution', color='white', fontsize=12, fontweight='bold')
        ax4.set_ylabel('Value (cm)', color='white')
        ax4.tick_params(colors='white')
        for spine in ax4.spines.values():
            spine.set_color('white')
        
        plt.tight_layout()
        
        # Save to buffer
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=150, facecolor='#1a1a2e', 
                   edgecolor='none', bbox_inches='tight')
        buf.seek(0)
        plt.close(fig)
        
        # Convert to base64
        img_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
        return jsonify({'success': True, 'image': img_base64})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/chart/3d')
def chart_3d():
    """Generate 3D scatter plot of Iris dataset."""
    try:
        X, y, names, _ = get_iris_data()
        
        # Create 3D figure
        fig = plt.figure(figsize=(12, 10))
        fig.patch.set_facecolor('#1a1a2e')
        ax = fig.add_subplot(111, projection='3d')
        ax.set_facecolor('#16162a')
        
        colors = ['#FF6B9D', '#9B59B6', '#3498DB']
        
        # Plot each species
        for i, (color, name) in enumerate(zip(colors, names)):
            mask = y == i
            ax.scatter(X[mask, 0], X[mask, 1], X[mask, 2],
                      c=color, label=name.capitalize(),
                      alpha=0.8, edgecolors='white', s=80, depthshade=True)
        
        ax.set_xlabel('Sepal Length (cm)', color='white', labelpad=10)
        ax.set_ylabel('Sepal Width (cm)', color='white', labelpad=10)
        ax.set_zlabel('Petal Length (cm)', color='white', labelpad=10)
        ax.set_title('3D Iris Dataset Visualization', color='white', 
                    fontsize=14, fontweight='bold', pad=20)
        
        # Style the axes
        ax.tick_params(colors='white')
        ax.xaxis.pane.fill = False
        ax.yaxis.pane.fill = False
        ax.zaxis.pane.fill = False
        ax.xaxis.pane.set_edgecolor('white')
        ax.yaxis.pane.set_edgecolor('white')
        ax.zaxis.pane.set_edgecolor('white')
        ax.xaxis._axinfo['grid']['color'] = '#444466'
        ax.yaxis._axinfo['grid']['color'] = '#444466'
        ax.zaxis._axinfo['grid']['color'] = '#444466'
        
        ax.legend(facecolor='#1a1a2e', edgecolor='white', labelcolor='white',
                 loc='upper left', fontsize=10)
        
        # Rotate for better view
        ax.view_init(elev=20, azim=45)
        
        # Save to buffer
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=150, facecolor='#1a1a2e',
                   edgecolor='none', bbox_inches='tight')
        buf.seek(0)
        plt.close(fig)
        
        img_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
        return jsonify({'success': True, 'image': img_base64})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/chart/3d/pca')
def chart_3d_pca():
    """Generate 3D PCA visualization."""
    try:
        X, y, names, _ = get_iris_data()
        
        # Apply PCA
        pca = PCA(n_components=3)
        X_pca = pca.fit_transform(X)
        
        # Create 3D figure
        fig = plt.figure(figsize=(12, 10))
        fig.patch.set_facecolor('#1a1a2e')
        ax = fig.add_subplot(111, projection='3d')
        ax.set_facecolor('#16162a')
        
        colors = ['#FF6B9D', '#9B59B6', '#3498DB']
        
        for i, (color, name) in enumerate(zip(colors, names)):
            mask = y == i
            ax.scatter(X_pca[mask, 0], X_pca[mask, 1], X_pca[mask, 2],
                      c=color, label=name.capitalize(),
                      alpha=0.8, edgecolors='white', s=80)
        
        ax.set_xlabel(f'PC1 ({pca.explained_variance_ratio_[0]*100:.1f}%)', 
                     color='white', labelpad=10)
        ax.set_ylabel(f'PC2 ({pca.explained_variance_ratio_[1]*100:.1f}%)', 
                     color='white', labelpad=10)
        ax.set_zlabel(f'PC3 ({pca.explained_variance_ratio_[2]*100:.1f}%)', 
                     color='white', labelpad=10)
        ax.set_title('3D PCA Visualization', color='white',
                    fontsize=14, fontweight='bold', pad=20)
        
        ax.tick_params(colors='white')
        ax.xaxis.pane.fill = False
        ax.yaxis.pane.fill = False
        ax.zaxis.pane.fill = False
        ax.xaxis.pane.set_edgecolor('white')
        ax.yaxis.pane.set_edgecolor('white')
        ax.zaxis.pane.set_edgecolor('white')
        
        ax.legend(facecolor='#1a1a2e', edgecolor='white', labelcolor='white')
        ax.view_init(elev=25, azim=135)
        
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=150, facecolor='#1a1a2e',
                   edgecolor='none', bbox_inches='tight')
        buf.seek(0)
        plt.close(fig)
        
        img_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
        return jsonify({'success': True, 'image': img_base64})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/predict', methods=['POST'])
def api_predict():
    """API endpoint for predictions (returns JSON)."""
    if model is None:
        return jsonify({'error': 'Model not loaded'}), 500
    
    try:
        data = request.get_json()
        features = [
            float(data['sepal_length']),
            float(data['sepal_width']),
            float(data['petal_length']),
            float(data['petal_width'])
        ]
        
        input_features = np.array([features])
        prediction_idx = model.predict(input_features)[0]
        prediction_proba = model.predict_proba(input_features)[0]
        
        flower_name = target_names[prediction_idx]
        confidence = prediction_proba[prediction_idx] * 100
        
        return jsonify({
            'success': True,
            'prediction': flower_name.capitalize(),
            'confidence': f"{confidence:.1f}%",
            'probabilities': {
                name.capitalize(): f"{prob * 100:.1f}%" 
                for name, prob in zip(target_names, prediction_proba)
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/stats')
def api_stats():
    """Return dataset statistics."""
    try:
        X, y, names, feature_names = get_iris_data()
        
        stats = {
            'total_samples': len(X),
            'features': list(feature_names),
            'classes': [name.capitalize() for name in names],
            'samples_per_class': {
                name.capitalize(): int(np.sum(y == i))
                for i, name in enumerate(names)
            },
            'feature_stats': {
                fname: {
                    'min': round(float(X[:, i].min()), 2),
                    'max': round(float(X[:, i].max()), 2),
                    'mean': round(float(X[:, i].mean()), 2),
                    'std': round(float(X[:, i].std()), 2)
                }
                for i, fname in enumerate(feature_names)
            }
        }
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    if model is None:
        print("⚠️  Warning: Model not loaded. Run 'python train_model.py' first!")
    else:
        print("✅ Model loaded successfully!")
    
    print("\n" + "=" * 50)
    print("🌸 IRIS FLOWER PREDICTOR - ENHANCED")
    print("=" * 50)
    print("🚀 Starting Flask server...")
    print("📍 Open http://127.0.0.1:5000 in your browser")
    print("📊 Charts: /chart/2d, /chart/3d, /chart/3d/pca")
    print("=" * 50 + "\n")
    
    app.run(debug=True, port=5000, threaded=True)
