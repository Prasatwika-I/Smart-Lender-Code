# Smart Lender - Loan Eligibility Prediction System

Smart Lender is a complete, production-ready Flask web application designed to help applicants estimate their loan eligibility. By evaluating key personal and financial parameters, the system leverages a pre-trained XGBoost machine learning model to provide an instant eligibility classification under a premium banking interface.

---

## 🏦 UI/UX Design Theme
- **Theme**: Premium Banking (Corporate Blue and White).
- **Styling**: Minimal, clean, responsive, and mobile-optimized using Bootstrap 5, custom styles, and subtle micro-interactions.
- **Form Grouping**: Single-page form grouped into intuitive panels:
  - **Applicant Information**: Gender, Married, Dependents, Education, and Self Employed status.
  - **Financial Information**: Applicant Income, Coapplicant Income, Loan Amount, Loan Term, Credit History, and Property Area.

---

## 🛠️ Technology Stack
- **Backend Framework**: Python, Flask
- **Machine Learning**: XGBoost, Scikit-learn (loaded via `pickle`)
- **Data Manipulation**: Pandas, NumPy
- **Frontend Styling**: HTML5, CSS3, JavaScript, Bootstrap 5, Bootstrap Icons

---

## 📂 Project Structure
```text
Smart Lender/
├── app.py                  # Main Flask server, routing, and prediction logic
├── dataset/
│   └── loan_prediction.csv  # Historical bank loan dataset
├── loan_model.pkl          # Pre-trained XGBoost loan prediction model
├── requirements.txt        # Python package dependencies
├── templates/
│   ├── home.html           # Professional banking landing page
│   ├── predict.html        # Clean, single-page grouped credit form
│   └── result.html         # Status cards (Approved / Rejected) with credit summaries
└── static/
    ├── css/
    │   └── style.css       # Premium banking custom stylesheets
    ├── js/
    │   └── main.js         # Validation checks and submit spinner logic
    └── images/
        └── loan_banking_illustration.png  # Hero section vector illustration
```

---

## 🚀 How to Run Locally

### 1. Prerequisite
Ensure you have Python 3.10+ installed.

### 2. Install Dependencies
Open your terminal in the project workspace and run:
```bash
pip install -r requirements.txt
```

### 3. Run the Flask Server
Start the application by running:
```bash
python app.py
```

### 4. Access the Application
Open your browser and navigate to:
[http://localhost:5000/](http://localhost:5000/)

---

## 🌐 Cloud Deployment Options

### Option 1: Render (Recommended - Free / Easy)
1. Push your code to a GitHub repository.
2. Go to [Render Dashboard](https://dashboard.render.com/) and create a **New Web Service**.
3. Connect your repository.
4. Set:
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`

### Option 2: Railway / Heroku
- The repository already includes a [`Procfile`](file:///c:/Smart%20Lender/Procfile) configured with `gunicorn`. Connecting your GitHub repository will automatically detect and deploy the web service.

### Option 3: Docker Container
Build and run the container locally or on any cloud container service (AWS ECS, GCP Cloud Run, Azure Container Apps):
```bash
docker build -t smart-lender .
docker run -p 5000:5000 smart-lender
```
