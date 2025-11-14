# 🌟 AI Copilot — Human‑in‑the‑Loop Educational Module Generator

> A production‑ready AI‑powered curriculum generation platform that blends **automation** with **human expertise**. Built with **Groq Llama‑3.1**, **Streamlit**, and **SQLite**, featuring a professional review workflow, versioning, and analytics dashboard.

---

## 🚀 Overview

**AI Copilot** is a modern educational content creation system designed to help instructors generate, review, edit, approve, and publish complete learning modules.  
It accelerates curriculum development using **high‑speed AI generation** and ensures quality using a **human‑in‑the‑loop review system**.

### ✔ What It Offers
- Fast, structured module generation (Learning Objectives, Lessons, Assessments)
- Side‑by‑side human vs AI editing
- Approval workflow for each section
- Version history and audit trails
- Real‑time analytics dashboard
- Persistent storage with SQLite

---

## ✨ Features

### 🧠 AI‑Powered Module Generation
- Uses **Groq — Llama‑3.1‑8B Instant** for ultra‑fast structured generation  
- Generates complete modules covering:
  - Learning Objectives (Bloom’s Taxonomy)
  - Lessons
  - Assessments

### ✍️ Human‑in‑the‑Loop Editing
- Compare AI‑generated & user‑edited content side by side  
- Section‑level actions:
  - **Accept**
  - **Reject** + comments
  - **Reset**
  - **Regenerate**

### 📚 Module Library
- Browsing, searching, sorting
- Version history of all modules
- Export capabilities

### 📊 Analytics Dashboard
- Module approval progress
- Rejection/acceptance metrics
- Completion tracking

### 💾 Persistent Storage
- SQLite database with:
  - modules  
  - sections  
  - approvals  
  - version history  
- Cascading deletes & referential integrity

---

## 🛠 Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | Streamlit |
| Backend | Python 3.10+ |
| LLM Engine | Groq Cloud — Llama‑3.1‑8B‑Instant |
| Database | SQLite |
| Visualization | Plotly, Pandas |
| Config | python‑dotenv |

### Key Dependencies
```
streamlit
groq
plotly
pandas
python-dotenv
```

---

## 📁 Folder Structure

```
AI Copilot_Human-in-the-Loop/
│ app.py
│ modules.db
│ requirements.txt
│ README.md
│ .env
│
├── prompts/
│   ├── curriculum.md
│   └── pedagogy.md
│
├── utils/
│   ├── database.py
│   ├── file_utils.py
│   └── test_db_buttons.py
│
├── sample_ai_output.json
└── approved_lessons.json
```

---

## 📦 Installation

### 1. Clone
```bash
git clone <repo-url>
cd AI Copilot_Human-in-the-Loop
```

### 2. Create Virtual Environment
```bash
python -m venv venv
```

### 3. Activate  
**Windows**
```powershell
.env\Scripts\Activate.ps1
```
**Mac/Linux**
```bash
source venv/bin/activate
```

### 4. Install Requirements
```bash
pip install -r requirements.txt
```

### 5. Configure Environment
Create `.env`:
```
GROQ_API_KEY=your_api_key
GROQ_MODEL=llama-3.1-8b-instant
```

---

## ▶ Running the App

```bash
streamlit run app.py --server.port=8501
```

Then open:

👉 http://localhost:8501

---

## 📚 Module Structure

```json
{
  "module_title": "",
  "sections": [
    {
      "section_id": "lo1",
      "type": "learning_objective",
      "title": "",
      "content": "",
      "bloom_level": ""
    },
    {
      "section_id": "lesson1",
      "type": "lesson",
      "title": "",
      "content": ""
    },
    {
      "section_id": "assessment1",
      "type": "assessment",
      "title": "",
      "content": ""
    }
  ]
}
```

---

## 🤖 AI Model Information

| Property | Value |
|----------|-------|
| Model | llama‑3.1‑8b‑instant |
| Provider | Groq Cloud |
| Speed | ~100ms |
| Context | 8K tokens |

### Built‑In Reliability
- 3 retry attempts with backoff  
- JSON validation  
- Markdown stripping  
- Detailed error messages  

---

## 📸 Screenshots / Demo
(Add your screenshots here)

- Dashboard  
- Generate page  
- Editor view  
- Analytics  

---

## 🤝 Contributing

1. Fork → Clone → Create new branch  
2. Follow **PEP8** coding style  
3. Submit PR with clear description  

### Areas to Contribute
- UI/UX improvements  
- Multi-user system  
- RBAC  
- More analytics  
- Better regression tests  

---

## 📜 License
Released under the **MIT License**.

---

## 📧 Contact

**Project Maintainer:** AI Copilot Team  
**Email:** contact@aicopilot.example.com  

---

## 🛠 Troubleshooting

### Port in Use
```
streamlit run app.py --server.port=8502
```

### Database Locked
Close Python processes:
```powershell
Get-Process python | Stop-Process -Force
```

### Invalid JSON
- Check `.env`
- Verify API key  
- Try regenerating module  

---

**Last Updated:** November 2025  
**Status:** Production‑Ready ✔
