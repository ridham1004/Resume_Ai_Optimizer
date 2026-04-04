# 🚀 AI Resume Optimizer
**Theme:** Innovate Beyond Boundaries 

An intelligent, multi-agent AI system designed to perfectly tailor your LaTeX resume and cover letter to any target job description without hallucinating or breaking strict spatial formatting constraints.

## 💡 The Problem & Solution
Job seekers often struggle to tailor their resumes for specific roles without breaking the strict formatting of their LaTeX templates or accidentally fabricating information. 

**The AI Resume Optimizer** solves this by using a "Source of Truth" Data Pool. Two specialized AI agents (powered by Google's Vertex AI) analyze the target Job Description, extract the most relevant metrics and skills from your master data pool, and seamlessly inject them into a beautifully formatted, heavily constrained LaTeX template. It intelligently fits your best experiences into strict spatial limits.

## 🛠️ Tech Stack
* **Backend:** Python, FastAPI, Uvicorn
* **AI Engine:** Google Cloud Vertex AI (Gemini 1.5 Flash)
* **Frontend:** HTML, Tailwind CSS (Designed via Google Stitch)
* **Output:** Compilable LaTeX (`.tex`) documents ready for Overleaf

## ⚙️ Prerequisites
Before running this project, ensure you have:
1. Python 3.10+ installed.
2. A Google Cloud Project with the **Vertex AI API** enabled.
3. Google Cloud credentials configured on your local machine (via `gcloud auth application-default login`).

## 🚀 Quick Start Guide

### 1. Installation
Clone the repository and set up your virtual environment:
```bash
git clone [https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git](https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git)
cd innovate-resume-ai
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt