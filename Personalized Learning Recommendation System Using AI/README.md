# 🎓 Personalized Learning Path Recommendation System

> **Project BT3116 · IILM University, Greater Noida · Session 2025–26**

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)](https://python.org)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange?logo=jupyter)](https://jupyter.org)
[![Gradio](https://img.shields.io/badge/UI-Gradio-ff6b6b?logo=gradio)](https://gradio.app)
[![scikit-learn](https://img.shields.io/badge/ML-scikit--learn-f7931e?logo=scikit-learn)](https://scikit-learn.org)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

---

## 👥 Team

| Name | Role |
|------|------|
| Swastik Srivastava | Developer |
| Stuty Singh | Developer |
| Suryansh Singh | Developer |
| Suprit Dubey | Developer |
| Tanisha Priya | Developer |

**Faculty Guide:** Dr. Jaswinder Singh Walia

---

## 📌 Overview

An AI-powered **Content-Based Filtering** recommender system that generates personalized learning paths for students. Given a course a student has completed or is currently taking, the system recommends the most relevant next courses using **TF-IDF Vectorization** and **Cosine Similarity**, visualizes the path as a **DAG (Directed Acyclic Graph)**, and evaluates quality using standard IR metrics.

---

## 🧠 How It Works

```
User selects a course
        │
        ▼
Feature Engineering
(category × 3, level weight, Bloom taxonomy, skills × 2, prerequisites, duration tag)
        │
        ▼
TF-IDF Vectorization
(bigram, sublinear_tf=True, max_features=500, stop_words=english)
        │
        ▼
Cosine Similarity Matrix (20 × 20)
        │
        ▼
Top-K Recommendations + Natural Language Explanations
        │
        ▼
DAG Learning Path (NetworkX + Plotly)
        │
        ▼
Gradio Interactive UI
```

---

## 📊 Dataset

20 curated courses across 6 domains, each with 7 attributes:

| Domain | Courses |
|--------|---------|
| Programming | Python Fundamentals, DSA |
| Data Science | Statistics, SQL, Pandas |
| AI / ML | ML Fundamentals, Deep Learning, NLP, CV, RL, MLOps |
| Web Development | HTML/CSS, JavaScript, React.js, Node.js, Full Stack |
| Cloud Computing | AWS, Docker & Kubernetes |
| Security | Cybersecurity Essentials, Ethical Hacking |

**Attributes:** `name`, `category`, `level`, `bloom_level`, `skills`, `duration`, `prerequisites`

---

## ⚙️ Tech Stack

| Component | Technology |
|-----------|-----------|
| Language | Python 3.8+ |
| ML / NLP | scikit-learn (TF-IDF, Cosine Similarity) |
| Data | pandas, numpy |
| Graph | NetworkX |
| Visualization | Plotly, Matplotlib |
| UI | Gradio |
| Notebook | Jupyter |

---

## 📈 Evaluation Metrics

The system is evaluated at K = 1, 3, 5, 7, 10 using:

- **Precision@K** — fraction of top-K recommendations that are relevant
- **MAP@K** — Mean Average Precision at K
- **NDCG@K** — Normalized Discounted Cumulative Gain at K

Ground truth: courses in the same category **or** connected via prerequisite chains are considered relevant.

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/BT3116_LearningRecommender.git
cd BT3116_LearningRecommender
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the notebook

```bash
jupyter notebook BT3116_Personalized_Learning_Recommender.ipynb
```

Or run the app directly:

```bash
python app.py
```

---

## 🖥️ Gradio UI Features

- **Course Selector** — choose from 20 available courses
- **Top-K Slider** — get 1–10 recommendations
- **Domain Filter** — narrow results by category
- **Level Filter** — filter by Beginner / Intermediate / Advanced
- **Recommendations Tab** — ranked cards with similarity scores and explanations
- **DAG Tab** — interactive Plotly learning path graph

---

## 📁 Project Structure

```
BT3116_LearningRecommender/
│
├── BT3116_Personalized_Learning_Recommender.ipynb   # Main notebook
├── app.py                                            # Standalone Gradio app
├── recommender.py                                    # Core recommendation logic
├── requirements.txt                                  # Python dependencies
├── README.md                                         # This file
└── LICENSE                                           # MIT License
```

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).

---

> *IILM University · School of Computer Science & Engineering · Greater Noida*
