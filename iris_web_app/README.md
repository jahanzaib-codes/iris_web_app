# 🌸 Iris Flower Predictor

A beautiful web application that uses Machine Learning to predict Iris flower species based on sepal and petal measurements.

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Flask](https://img.shields.io/badge/Flask-2.0+-green)
![ML](https://img.shields.io/badge/ML-KNN-purple)
![Joblib](https://img.shields.io/badge/Joblib-Model%20Saving-orange)

## ✨ Features

- 🔮 **ML Prediction**: KNN classifier trained on the Iris dataset
- 🌙 **Dark Mode**: Toggle between light and dark themes
- 🎨 **Beautiful UI**: Modern design with gradients and animations
- 📱 **Responsive**: Works on desktop and mobile devices
- 💾 **Theme Persistence**: Saves your theme preference in localStorage
- ⚡ **Joblib**: Uses joblib for efficient model serialization

## 📁 Project Structure

```
iris_web_app/
│
├── app.py              # Flask application
├── train_model.py      # ML model training script
├── model.joblib        # Trained model (generated after training)
├── target_names.joblib # Class labels (generated after training)
├── requirements.txt    # Python dependencies
├── .gitignore          # Git ignore file
├── README.md           # This file
│
├── templates/
│   └── index.html      # Web UI template
│
└── static/
    ├── css/
    │   └── style.css   # Styling with dark mode
    └── js/
        └── theme.js    # Dark mode toggle logic
```

---

## 🚀 Installation & Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/iris-flower-predictor.git
cd iris-flower-predictor
```

### Step 2: Create Virtual Environment (Recommended)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Train the Model

```bash
python train_model.py
```

This will:
- Load the Iris dataset
- Train a KNN classifier
- Save the model as `model.joblib`

### Step 5: Run the Application

```bash
python app.py
```

### Step 6: Open in Browser

Navigate to: **http://127.0.0.1:5000**

---

## 📤 GitHub Par Upload Kaise Karein (Step by Step)

### ✅ Pre-requisites:
1. GitHub account hona chahiye: [github.com](https://github.com)
2. Git installed hona chahiye: [git-scm.com](https://git-scm.com/downloads)

### 📝 Step-by-Step Guide:

#### Step 1: Git Initialize karein
```bash
cd iris_web_app
git init
```

#### Step 2: Apni files add karein
```bash
git add .
```

#### Step 3: First commit karein
```bash
git commit -m "Initial commit: Iris Flower Predictor with ML and Dark Mode"
```

#### Step 4: GitHub par new repository banayein
1. GitHub.com par jayein
2. **"+"** icon par click karein (top right)
3. **"New repository"** select karein
4. Repository name dein: `iris-flower-predictor`
5. Description dein (optional): `🌸 Iris Flower Prediction Web App with ML and Dark Mode`
6. **Public** ya **Private** choose karein
7. **"Create repository"** button dabayein

#### Step 5: GitHub repository ko local ke saath connect karein
```bash
git remote add origin https://github.com/YOUR_USERNAME/iris-flower-predictor.git
```
> ⚠️ `YOUR_USERNAME` ko apne GitHub username se replace karein

#### Step 6: Branch rename karein main par (agar pehle se nahi hai)
```bash
git branch -M main
```

#### Step 7: Push karein (Upload)
```bash
git push -u origin main
```

#### Step 8: Credentials enter karein
- Username: Apna GitHub username
- Password: GitHub Personal Access Token (PAT)

> 📌 **Note**: GitHub ab password accept nahi karta, PAT use karna padega.

### 🔑 Personal Access Token (PAT) Kaise Banayein:
1. GitHub → **Settings** → **Developer settings**
2. **Personal access tokens** → **Tokens (classic)**
3. **"Generate new token"** click karein
4. Note dein: `git-access`
5. Expiration: 90 days ya jitna chahein
6. Scopes select karein: ✅ `repo` (full control)
7. **"Generate token"** click karein
8. Token copy karein aur safe rakkhein (yeh dobara nahi dikhega!)

### ✅ All Done!
Ab aapka project GitHub par upload ho gaya hai! 🎉

URL hoga: `https://github.com/YOUR_USERNAME/iris-flower-predictor`

---

## 🔄 Future Updates Upload Karne Ke Liye

```bash
# Changes add karein
git add .

# Commit karein
git commit -m "Your update message here"

# Push karein
git push origin main
```

---

## 🎯 How to Use the App

1. Enter the flower measurements:
   - Sepal Length (cm)
   - Sepal Width (cm)
   - Petal Length (cm)
   - Petal Width (cm)

2. Click **"Predict Species"**

3. View the prediction result with confidence percentage

4. Toggle **Dark Mode** using the 🌙/☀️ button in the navbar

---

## 🌸 Iris Species

| Species | Description |
|---------|-------------|
| 🌸 Setosa | Small, delicate petals with distinctive purple/blue coloring |
| 🌺 Versicolor | Also called "Blue Flag", features beautiful purple-blue flowers |
| 🌷 Virginica | The largest species with striking violet-blue flowers |

---

## 🛠️ Technologies Used

| Technology | Purpose |
|------------|---------|
| **Flask** | Python Web Framework |
| **scikit-learn** | Machine Learning (KNN) |
| **joblib** | Model Serialization (better than pickle) |
| **HTML5/CSS3** | Frontend Structure & Styling |
| **JavaScript** | Dark Mode Toggle & Animations |
| **Google Fonts** | Inter font family |

---

## 📊 Model Details

- **Algorithm**: K-Nearest Neighbors (KNN)
- **K Value**: 3
- **Dataset**: Iris (150 samples, 4 features, 3 classes)
- **Accuracy**: ~96-98%
- **Model Format**: joblib (more efficient than pickle for numpy arrays)

---

## 🔌 API Endpoint

For programmatic access:

```bash
POST /api/predict
Content-Type: application/json

{
    "sepal_length": 5.1,
    "sepal_width": 3.5,
    "petal_length": 1.4,
    "petal_width": 0.2
}
```

Response:
```json
{
    "success": true,
    "prediction": "Setosa",
    "confidence": "100.0%",
    "probabilities": {
        "Setosa": "100.0%",
        "Versicolor": "0.0%",
        "Virginica": "0.0%"
    }
}
```

---

## 🤔 Joblib vs Pickle - Kyun Joblib?

| Feature | Pickle | Joblib |
|---------|--------|--------|
| **Speed** | Slower | Faster for large arrays |
| **Compression** | No | Yes |
| **sklearn optimized** | No | Yes |
| **Memory efficient** | No | Yes |

---

## 👨‍💻 Author

Built with 💜 using Flask & Machine Learning

---

## 📜 License

This project is open source and available under the MIT License.

---

**Happy Predicting! 🌸**
