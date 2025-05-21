# 🧠 Breast Cancer Predictor App (Streamlit + ML)

An intelligent, user-friendly web application for predicting breast cancer using machine learning. Built with **Streamlit**, it allows users to input data manually or upload CSV files for batch prediction. The app provides a stylish dark-themed UI, user authentication, and data visualization.

---

## 📌 Project Overview

This project aims to assist in the early detection of breast cancer using a supervised machine learning model trained on the **Wisconsin Breast Cancer Diagnostic Dataset**. It provides two main functionalities:

- **Single Prediction** – Users can input features through sliders.
- **Batch Prediction** – Upload a CSV file and receive predictions for multiple records.

**Key Features:**
- Streamlit-based interactive frontend
- Custom dark theme with CSS
- User authentication (Login/Registration)
- Batch diagnosis using uploaded CSV
- Real-time result display
- SHAP explanations (optional/future)
- Code is modular and well-documented

---

## ⚙️ Setup Instructions

> Ensure you have Python 3.8+ installed.

1. **Clone the Repository**

```bash
git clone https://github.com/juliuslaggah/breast-cancer-predictor.git
cd breast-cancer-predictor
```

2. **Create and Activate a Virtual Environment**

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

3. **Install Dependencies**

```bash
pip install -r requirements.txt
```

---

## 📦 Dependencies

Here are the main packages used:

```
streamlit
scikit-learn
pandas
matplotlib
shap             # Optional for XAI
joblib
plotly           # For radar chart visualization
```

Install them manually (if needed):

```bash
pip install streamlit scikit-learn pandas matplotlib shap joblib plotly
```

---

## 🚀 How to Run the App

From the project root directory, run:

```bash
streamlit run app/main.py
```

Then open the URL provided by Streamlit in your browser.

---

## 🖼️ Sample Screenshots

<details>
<summary>🔐 Login Page</summary>

![Login Page](assets/login.png)

</details>

<details>
<summary>📊 Single Prediction</summary>

![Single Prediction](assets/newplot.png)

</details>

<details>
<summary>📁 Batch Prediction with CSV</summary>

![Batch Prediction](assets/batch_prediction.png)

</details>

> You can add these images in a `screenshots` folder inside your repo.

---

## 📄 Report

The full project report is available [here](report/Breast_Cancer_Predictor_Report.docx)  
> _(Ensure you upload the Word file inside a `report/` folder in the repository)_

---

## 👥 Authors

- Julius Laggah— Backend, Model Integration, Project Lead
- Sadar Win
- Adamsay Turay
- Jusu Abdul Karim


---

## ✅ License

This project is open-source and available under the GPL v.3 License.

[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/streamlit-v1.18.1-orange)](https://streamlit.io/)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE)

