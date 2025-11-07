
# 🛡️ Phishing Email Detection using Machine Learning

A full-stack **Phishing Email Detection System** that uses **Deep Learning (LSTM)** and **URL-based feature extraction** to classify emails as *Phishing* or *Legitimate*.  
The project includes a Flask-based web interface for users to paste email content and get real-time predictions.  
It is deployed live on **Railway.app**, integrated directly with GitHub for continuous deployment.

---

## 🌐 Live Demo

🔗 **App URL:** [https://web-production-4236.up.railway.app/](https://web-production-4236.up.railway.app/)
📦 **GitHub Repository:** [https://github.com/susa0676/Phishing-detection](https://github.com/susa0676/Phishing-detection)

---

## 📘 Project Overview

This project detects phishing emails using a hybrid machine learning model that combines:
- **Natural Language Processing (NLP)** on email text (via LSTM)
- **URL feature extraction** using domain heuristics (length, HTTPS, TLD, keywords, etc.)
- **Interaction features** that amplify phishing or safety signals

The trained model is integrated into a **Flask web application** with a responsive frontend.  
Users can paste any suspicious email content and instantly receive predictions such as:

> **Result:** 🧠 "Phishing Email"  
> **Confidence Score:** 96.27%

---

## 🧠 Model Architecture

- **Text Branch:** LSTM layers process cleaned email text sequences.
- **URL Feature Branch:** Dense layers process numerical URL & text-based features.
- **Fusion Layer:** Concatenates both outputs and passes through dense layers.
- **Output:** Binary classification (Phishing = 1, Legitimate = 0).

The system extracts 14 engineered features such as:
```

url_length, has_https, num_dots, has_at, has_ip,
is_shortened, has_suspicious_kw, uncommon_tld,
domain_length, phish_kw_count, legit_kw_count,
lure_url_interaction, safety_amplifier

```

---

## 🧩 Repository Structure
```

📦 phishing-email-detection
┣ 📂 models/                     # Saved model and feature files
┣ 📂 templates/                  # HTML templates (index.html)
┣ 📂 static/                     # CSS / JS assets
┣ 📜 app.py                      # Flask web app entry point
┣ 📜 predict.py                  # Model loading & inference logic
┣ 📜 preprocess.py               # Cleaning & feature extraction
┣ 📜 train_model.py              # Model training and evaluation
┣ 📜 requirements.txt            # Python dependencies
┣ 📜 Procfile                    # Railway/Render startup command
┗ 📜 README.md                   # You're here!

````

---

## ⚙️ Installation (Run Locally)

### 1️⃣ Clone the repository
```bash
git clone https://github.com/SudharsananGanapathy/phishing-email-detection.git
cd phishing-email-detection
````

### 2️⃣ Create a virtual environment

```bash
python -m venv .venv
# Activate
.venv\Scripts\activate   # Windows
source .venv/bin/activate   # Linux/Mac
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Run the Flask app

```bash
python app.py
```

Then visit: **[http://127.0.0.1:5000/](http://127.0.0.1:5000/)**

---

## 🚀 Deployment (Railway)

The app is deployed using [Railway.app](https://railway.app/), a cloud platform for web services.

### Deployment configuration:

**Procfile**

```
web: gunicorn app:app -w 1 -k gthread --threads 2 --timeout 300
```

**Port**

```bash
PORT=8080
```

**Memory Settings**

> Recommended: 1–2 GB RAM for TensorFlow inference stability.

---

## 🧪 Example Inputs

### 🟥 **Phishing Email Example**

```
Dear User,
Your account has been suspended due to suspicious login attempts.
Please verify your information at http://secure-login-update.xyz/verify immediately.
```

**Output:** 🧠 “Phishing” — Confidence: 97.41%

---

### 🟩 **Legitimate Email Example**

```
Hi Team,
Please find attached the project meeting minutes and the updated schedule.
Let’s finalize the design review by Friday.
Regards,
Sudharsanan
```

**Output:** ✅ “Legitimate” — Confidence: 93.88%

---

## 🧰 Technologies Used

| Component         | Technology                               |
| ----------------- | ---------------------------------------- |
| **Language**      | Python 3.10                              |
| **Frameworks**    | Flask, TensorFlow / Keras                |
| **Libraries**     | Pandas, Scikit-learn, Joblib, TLDExtract |
| **Frontend**      | HTML, CSS, Bootstrap                     |
| **Deployment**    | Railway.app                              |
| **Visualization** | Matplotlib, Seaborn                      |

---

## 🧩 Key Features

✅ Real-time phishing email detection
✅ Hybrid LSTM + URL feature fusion model
✅ Responsive web interface
✅ Lazy-loaded TensorFlow model (optimized for deployment)
✅ Deployed seamlessly via Railway with GitHub CI/CD

---

## 📊 Training Results

| Metric    | Score     |
| --------- | --------- |
| Accuracy  | **96.7%** |
| Precision | **95.2%** |
| Recall    | **97.9%** |
| F1-Score  | **96.5%** |

**Confusion Matrix Visualized**

| Actual ↓ / Predicted → | Legitimate | Phishing |
| ---------------------- | ---------- | -------- |
| **Legitimate**         | 120        | 4        |
| **Phishing**           | 3          | 123      |

---

## 📜 License

This project is licensed under the **MIT License** — free for educational and research use.

---

## 👨‍💻 Author

**Sudharsanan Ganapathy**
📫 [GitHub Profile](https://github.com/SudharsananGanapathy)
🎓 IT Student | AI & Cybersecurity Enthusiast
🚀 Guided Project: *Phishing Email Detection System using Hybrid Neural Network*
**AS Milton**
🎓 IT Student | AI & Cybersecurity Enthusiast
**Kulasekara Muthu**
🎓 IT Student | AI & Cybersecurity Enthusiast
**Saravanan A**
🎓 IT Student | AI & Cybersecurity Enthusiast
**Sathish K**
🎓 IT Student | AI & Cybersecurity Enthusiast
---

## ❤️ Acknowledgements

* TensorFlow & Keras for deep learning backbone
* Scikit-learn for preprocessing tools
* Flask for web integration
* Railway for deployment hosting

---

## 🧠 Future Enhancements

* Integrate Transformer-based (BERT) text encoding
* Add email header + sender domain analysis
* Include real-time URL verification (blacklist API)
* Deploy model as REST microservice on Cloud Run for scalable inference

---

## 🧾 Citation (for reports or papers)

> Sudharsanan, G. (2025). *Phishing Email Detection using Machine Learning (LSTM + URL Feature Fusion)*.
> GitHub Repository: [https://github.com/susa0676/Phishing-detection](https://github.com/susa0676/Phishing-detection)

---

