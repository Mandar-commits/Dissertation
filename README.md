---

# 🚀 AI Recruitment System

**Intelligent Resume Screening & Candidate Matching Platform**

---

## 📌 Project Overview

The **AI Recruitment System** is an end-to-end intelligent resume analysis and candidate ranking platform designed to automate the recruitment screening process using **Natural Language Processing (NLP)** and optional **Local LLM integration**.

The system extracts structured information from resumes, normalizes skills using a taxonomy, evaluates candidate relevance against job descriptions, and ranks candidates based on semantic similarity and skill matching.

This project was developed as part of a **Master’s Dissertation** focusing on applied NLP in HR automation.

---

## 🎯 Problem Statement

Manual resume screening is:

* Time-consuming
* Biased
* Inconsistent
* Difficult to scale

This system addresses these issues by:

* Automating resume ingestion
* Extracting and standardizing skills
* Matching candidates to job descriptions
* Ranking candidates objectively

---

## 🧠 System Architecture

```
                +------------------+
                |   Resume Input   |
                | (PDF / Text OCR) |
                +--------+---------+
                         |
                         v
                +------------------+
                | Text Extraction  |
                | (PDF Parser/OCR) |
                +--------+---------+
                         |
                         v
                +------------------+
                | Skill Extraction |
                | (spaCy / Rules)  |
                +--------+---------+
                         |
                         v
                +----------------------+
                | Skill Normalization  |
                | (Taxonomy Mapping)   |
                +--------+-------------+
                         |
                         v
                +----------------------+
                | Candidate Scoring    |
                | (Similarity Metrics) |
                +--------+-------------+
                         |
                         v
                +----------------------+
                | Ranked Candidates    |
                +----------------------+
```

---

## 🛠️ Tech Stack

| Layer                | Technology                      |
| -------------------- | ------------------------------- |
| Programming Language | Python 3.x                      |
| NLP Framework        | spaCy                           |
| OCR                  | Tesseract / pdf2image           |
| LLM (Optional)       | Ollama (Mistral / Local Models) |
| Backend Architecture | Modular (core, domain, app)     |
| Testing              | Pytest                          |
| Logging              | Python Logging                  |
| UI (if enabled)      | Flask / Frontend Module         |

---

## 📂 Project Structure

```
Dissertation/
│
├── app/                # Application entry point
├── core/               # Core business logic
├── domain/             # Domain models
├── ui/                 # UI module (if enabled)
├── validators/         # Resume ingestion & validation
├── utils/              # Utility helpers
├── tests/              # Unit & integration tests
├── logs/               # System logs
└── requirements.txt
```

### Module Responsibilities

* **core/** → Skill extraction, normalization, scoring logic
* **domain/** → Candidate and job data models
* **validators/** → Resume ingestion pipeline
* **ui/** → Frontend interaction layer
* **tests/** → Automated testing suite

---

## ⚙️ Installation Guide

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/Mandar-commits/Dissertation.git
cd Dissertation
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Running the Application

### Run Main Application

```bash
python app/main.py
```

### Run Tests

```bash
pytest tests/
```

---

## 🔍 Core Features

### ✅ Resume Ingestion

* PDF detection
* OCR fallback if text extraction fails
* Structured text output

### ✅ Skill Extraction

* spaCy-based extraction
* Rule-based matching
* Named Entity Recognition

### ✅ Skill Normalization

* Skill taxonomy mapping
* Synonym resolution
* Standardized skill representation

### ✅ Candidate Ranking

* Job description comparison
* Similarity scoring
* Ranked output

### ✅ Optional LLM Integration

* Local LLM extraction support
* Enhanced contextual understanding

---

## 📊 Evaluation Metrics

The system can be evaluated using:

* Precision
* Recall
* F1 Score
* Matching Accuracy
* Ranking Correlation

---

## 🧪 Testing Strategy

* Unit tests for skill extraction
* Validation tests for ingestion
* Integration tests for full pipeline
* Edge case testing (empty resume, OCR fallback)

---

## 🔐 Logging & Monitoring

* Structured logging
* Error handling for ingestion failures
* Debug logs for extraction pipeline

Logs are stored inside:

```
logs/
```

---

## 🚀 Future Enhancements

* Deep learning-based skill extraction (Transformer models)
* Bias detection & fairness evaluation
* Web-based recruiter dashboard
* Resume feedback generator
* Multi-language resume support
* REST API for enterprise integration
* Cloud deployment (AWS/GCP/Azure)
* Real-time analytics dashboard
* Automated interview question generation

---

## 📈 Research Contributions

* Practical application of NLP in HR automation
* Hybrid rule-based + AI architecture
* Modular and extensible design
* Scalable evaluation framework

---

## 📄 Dissertation Context

This project was developed as part of a postgraduate dissertation focusing on:

> **AI-driven recruitment automation using NLP and local language models**

---

## 👤 Author

Mandar Khollam
Master’s Dissertation Project
2025–2026

---

## 📜 License

This project is developed for academic and research purposes.

---

# ⭐ How to Improve This README Further (Optional Enhancements)

You may additionally add:

* Screenshots of UI
* Architecture diagram image
* Demo GIF
* Coverage badge
* GitHub Actions badge

---