
# Contributing to Breast Cancer Predictor

We welcome contributions to improve this project! Whether it's a bug fix, new feature, documentation update, or UI/UX suggestion — your input helps make this project better.

---

## 🧠 Project Overview

This is a Breast Cancer Diagnosis Predictor built using **Streamlit** and **Machine Learning**. It includes features like:
- **Manual Input** (cytology features via sliders)
- **Batch Prediction** (upload CSV)
- **DICOM Image Segmentation & Quantitative Features**
- **Dual-Model Architecture** (cytology-only & combined cytology+DICOM)
- **User Authentication** (Login / Register / Forgot Password)
- **Calibrated Probabilities** to avoid over-confidence
- **Dark-themed UI** with custom CSS


---

## 📋 Contribution Guidelines

### 1. Fork & Clone
- Fork this repository to your GitHub account.
- Clone it locally:
  ```bash
  git clone https://github.com/juliuslaggah/breast-cancer-predictor.git
  cd breast-cancer-predictor
  ```

### 2. Create a Branch
Name your feature or fix descriptively:
```bash
git checkout -b fix-login-bug
```

### 3. Write Clear Code
- Follow Pythonic standards (PEP8).
- Add docstrings and comments where necessary.
- Reuse helper functions in `utils.py` if applicable.
- Keep UI consistent with the dark-themed CSS (`style.css`).

### 4. Test Your Changes
- Run the app locally using:
  ```bash
  streamlit run app/main.py
  ```
- Test login/register, CSV uploads or dicom, and predictions.

### 5. Commit Changes
```bash
git add .
git commit -m "Fix login redirect issue after registration"
git push origin fix-login-bug
```

### 6. Create Pull Request
Go to GitHub and open a pull request from your branch. Clearly describe your change.

---

## 🧪 Reporting Bugs or Requesting Features

Open an [issue](https://github.com/your-username/breast-cancer-predictor/issues) and include:
- What you expected
- What happened
- Steps to reproduce
- (For features) why it adds value

---

## 🧑‍💻 Code of Conduct

We expect contributors to:
- Be respectful and constructive
- Communicate clearly
- Provide context in pull requests and issues

Harassment or discrimination of any kind will not be tolerated.

---

## 🧾 License

This project is under the GPL v.3 License. See `LICENSE` for details.

---

## 🙌 Thanks!

We appreciate your time and effort in contributing. Every bit helps improve the tool and potentially impacts early detection of breast cancer.
