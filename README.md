# 🌸 Iris Flower Predictor

A premium machine learning web application that classifies Iris flower species (Setosa, Versicolor, and Virginica) with high accuracy using a K-Nearest Neighbors (KNN) model.

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.0+-red)
![Flask](https://img.shields.io/badge/Flask-2.0+-green)
![Scikit--Learn](https://img.shields.io/badge/Scikit--Learn-Latest-orange)

## ✨ Unique Features

- 🧠 **Precision ML**: Powered by a finely-tuned KNN classifier.
- 📊 **Dynamic Visualizations**: Real-time 2D and 3D scatter plots of the Iris dataset.
- ✨ **PCA Analysis**: Interactive Principal Component Analysis visualization.
- 🎨 **Premium UI**: Modern design optimized for all devices.
- ⚡ **High Performance**: Optimized with Joblib for lightning-fast model loading.

## 🛠️ Technology Stack

| Component | Technology |
|-----------|------------|
| Backend   | Flask / Streamlit |
| ML Engine | Scikit-Learn (KNN) |
| Graphics  | Matplotlib |
| Analysis  | NumPy / PCA |
| Core Logic| Python 3.x |

## 📁 Project Structure

```text
iris_web_app/
├── streamlit_app.py    # Main Streamlit Application (Cloud Optimized)
├── app.py              # Flask Application (Web API & Alternative UI)
├── train_model.py      # Model Training Script
├── model.joblib        # Pre-trained ML Model
├── target_names.joblib # Species Label Mapping
├── requirements.txt    # Project Dependencies
└── static/             # Assets for Flask App
```

## 🚀 Installation & Setup

1. **Clone the project** to your local machine.
2. **Setup Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Train Model** (Optional, as model is pre-included):
   ```bash
   python train_model.py
   ```
5. **Run Application**:
   - For Streamlit: `streamlit run streamlit_app.py`
   - For Flask: `python app.py`

## 🎯 How To Use

1. **Enter Measurements**: Provide Sepal and Petal dimensions using the interactive sliders or fields.
2. **Analyze**: Click the **Predict** button to run the ML inference.
3. **Explore**: Navigate through the visualization tabs to see where your data point fits within the global Iris clusters.

## 🔧 Troubleshooting

| Issue | Solution |
|-------|----------|
| **Model not found** | Run `python train_model.py` to regenerate the `.joblib` files. |
| **ModuleNotFoundError** | Ensure all packages are installed via `pip install -r requirements.txt`. |
| **Streamlit Error** | Ensure you are running `streamlit run streamlit_app.py`. |
| **Port already in use** | Change the port in `app.py` or kill the process using that port. |

## ❓ FAQ

**Q: Which algorithm is used for prediction?**  
A: The app uses K-Nearest Neighbors (KNN), which is highly reliable for classification tasks with small-to-medium datasets.

**Q: Can I use this for other datasets?**  
A: Yes, the architecture is modular. You can modify `train_model.py` to train on any classification dataset.

**Q: Why Joblib instead of Pickle?**  
A: Joblib is optimized for objects containing large NumPy arrays, making it faster and more efficient for scikit-learn models.

## 📜 License

This project is licensed under the MIT License.

---
Built with ❤️ for Machine Learning Enthusiasts.
