# AI Copilot — Human-in-the-Loop

> **An intelligent educational module generator with human-in-the-loop editing, powered by Groq AI and Streamlit.**

Accelerate curriculum design with AI-powered module generation, intelligent editing, and approval workflows. Educators review, refine, and publish high-quality educational content at scale.

---

## 📑 Quick Navigation

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Quick Start](#-quick-start)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Running the App](#-running-the-app)
- [Project Structure](#-project-structure)
- [How It Works](#-how-it-works)
- [Module Details](#-module-details)
- [AI Model](#-ai-model)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)
- [Support](#-support)

---

## ✨ Features

**AI-Powered Content Generation**
- Generate complete educational modules (learning objectives, lessons, assessments)
- Customizable curriculum and pedagogy prompts
- AI model: Groq's `llama-3.1-8b-instant` (< 100ms latency)

**Human-in-the-Loop Editing**
- Side-by-side AI output vs. editable content review
- Section-level actions: Accept, Reject, Reset, Regenerate
- Detailed rejection comments and feedback tracking

**Version Control & Approval Workflow**
- Automatic version history for all edits
- Granular section-level approval status
- Approval/rejection timestamps and audit trails

**Module Management**
- Persistent SQLite database storage
- Module library with search and filtering
- One-click JSON export for all modules
- Analytics dashboard with real-time metrics

**Enterprise Quality**
- Cascading deletes and referential integrity
- Data consistency guarantees
- Robust retry logic with exponential backoff
- Comprehensive error handling

---

## 🛠️ Tech Stack

| Layer | Technology | Details |
|-------|-----------|---------|
| **Frontend** | Streamlit | Interactive web dashboard |
| **Backend** | Python 3.12 | Core application logic |
| **AI/LLM** | Groq Cloud API | `llama-3.1-8b-instant` model |
| **Database** | SQLite 3 | 4 normalized tables |
| **Visualization** | Plotly, Pandas | Charts and analytics |
| **Config** | python-dotenv | Environment-based configuration |

**Key Dependencies:**
```
streamlit>=1.28
groq>=0.4
python-dotenv>=1.0
plotly>=5.17
pandas>=2.0
```

See `requirements.txt` for complete list.

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+ (tested on 3.12)
- Windows PowerShell 5.1 (or bash on Linux/macOS)
- Groq API key (free at https://console.groq.com/keys)

### Get Running in 5 Minutes

```powershell
# 1. Clone or download the project
cd "C:\Users\Likith G S\Desktop\Dhumi Assignment\Dhumi_Assignment_4.2"

# 2. Create and activate virtual environment
python -m venv venv
& ".\venv\Scripts\Activate.ps1"

# 3. Install dependencies
pip install -r "AI Copilot_Human-in-the-Loop/requirements.txt"

# 4. Create .env file with your API key
@"
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.1-8b-instant
"@ | Out-File -Encoding UTF8 ".env"

# 5. Start the app
streamlit run "AI Copilot_Human-in-the-Loop/app.py"
```

Open browser to: **http://localhost:8501**

---

## 📥 Installation

### Step 1: Create Virtual Environment

```powershell
# Windows PowerShell
python -m venv venv
& ".\venv\Scripts\Activate.ps1"

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

### Step 2: Install Dependencies

```powershell
pip install --upgrade pip
pip install -r "AI Copilot_Human-in-the-Loop/requirements.txt"
```

### Step 3: Verify Installation

```powershell
python --version                    # Should be 3.10+
python -c "import groq; print('✓ Groq installed')"
python -c "import streamlit; print('✓ Streamlit installed')"
```

---

## ⚙️ Configuration

### Environment Variables

Create `.env` in your project root:

```dotenv
# Required
GROQ_API_KEY=gsk_your_actual_key_here

# Optional (has sensible default)
GROQ_MODEL=llama-3.1-8b-instant
```

### Getting Your API Key

1. Visit https://console.groq.com/keys
2. Sign in (or create account)
3. Create new API key
4. Copy to `.env` file

### Variable Reference

| Variable | Required | Default | Purpose |
|----------|----------|---------|---------|
| `GROQ_API_KEY` | ✅ Yes | — | Groq Cloud authentication |
| `GROQ_MODEL` | ❌ No | `llama-3.1-8b-instant` | LLM model selection |

---

## ▶️ Running the App

### Start the Application

```powershell
# Activate environment (if not already active)
& ".\venv\Scripts\Activate.ps1"

# Start Streamlit server
streamlit run "AI Copilot_Human-in-the-Loop/app.py" --server.port=8501
```

### Access Points

- **Local**: http://localhost:8501
- **Network**: http://<your-machine-ip>:8501

### Application Pages

**1️⃣ Generate Module**
- Create new modules with custom prompts
- Preview AI-generated content
- Save to database

**2️⃣ Editor** 
- Load and review generated modules
- Side-by-side comparison view
- Accept/Reject/Reset/Regenerate sections
- Real-time approval status

**3️⃣ Module Library**
- Browse all generated modules
- View approval status summary
- Export modules as JSON
- Access version history

**4️⃣ Analytics**
- Module completion rates
- Approval/rejection metrics
- Content quality insights
- Visual charts and statistics

---

## 📁 Project Structure

```
AI Copilot_Human-in-the-Loop/
│
├── app.py                      # Main Streamlit app (960 lines)
│                               # Handles all 4 pages and UI logic
│
├── modules.db                  # SQLite database (auto-created)
│                               # Tables: modules, sections, approvals, versions
│
├── .env                        # Environment configuration
│                               # Contains GROQ_API_KEY and GROQ_MODEL
│
├── requirements.txt            # Python dependencies
│
├── README.md                   # This file
│
├── prompts/
│   ├── curriculum.md           # Curriculum generation system prompt
│   └── pedagogy.md             # Pedagogical content system prompt
│
├── utils/
│   ├── file_utils.py           # Groq API wrapper (170 lines)
│   │                           # • generate_module()
│   │                           # • regenerate_content()
│   │                           # • summarize_changes()
│   │                           # • Retry logic with backoff
│   │
│   ├── database.py             # SQLite layer (290+ lines)
│   │                           # • CRUD operations
│   │                           # • Version tracking
│   │                           # • Approval workflows
│   │                           # • Statistics and exports
│   │
│   ├── test_db_buttons.py      # Database test helper (optional)
│   │
│   └── __pycache__/            # Python bytecode (safe to delete)
│
├── sample_ai_output.json       # Example generated module
│
└── approved_lessons.json       # Backup of published sections
```

---

## 🔄 How It Works

### Generation Pipeline

```
User Input (curriculum + pedagogy)
         ↓
    Groq API Call
    (with retries)
         ↓
    Parse JSON Response
    (with markdown unwrap)
         ↓
    Create Module Record
    in Database
         ↓
    Store in Session State
    for Preview
```

### Editing Workflow

```
Load Module from Database
         ↓
    Initialize Session State
    (normalize section IDs)
         ↓
    Display Side-by-Side View
    (AI output | editable content)
         ↓
    User Takes Action
    (Accept/Reject/Reset/Regenerate)
         ↓
    Create Version Record
    (track original → edited)
         ↓
    Update Approval Status
    (stored in database)
         ↓
    Display Real-Time Stats
```

### Data Flow

- **Session State**: Handles in-memory UI state (per user session)
- **Database**: Persistent storage (all modules, versions, approvals)
- **Version Table**: Complete edit history (original → new content)
- **Approvals Table**: Status tracking (approved/rejected/pending)

---

## 📚 Module Details

### Module Structure

Generated modules follow this JSON schema:

```json
{
  "module_title": "Name of the educational module",
  "sections": [
    {
      "section_id": "lo1",
      "type": "learning_objective",
      "title": "Section title",
      "content": "AI-generated content...",
      "bloom_level": "Knowledge|Comprehension|Application|Analysis|Synthesis|Evaluation"
    },
    {
      "section_id": "lesson1",
      "type": "lesson",
      "title": "Lesson name",
      "content": "Lesson content..."
    },
    {
      "section_id": "assessment1",
      "type": "assessment",
      "title": "Assessment name",
      "content": "Quiz/evaluation questions..."
    }
  ]
}
```

### Section Types

| Type | Purpose | Examples |
|------|---------|----------|
| **learning_objective** | Define what students will learn | `lo1`, `lo2`, `lo3` |
| **lesson** | Core instructional content | `lesson1`, `lesson2` |
| **assessment** | Evaluation and testing | `assessment1`, `assessment2` |

### Bloom's Taxonomy Integration

All learning objectives are aligned with Bloom's six levels:

- **Knowledge** — Recall facts and definitions
- **Comprehension** — Explain and interpret concepts
- **Application** — Use knowledge in new situations
- **Analysis** — Break down and examine components
- **Synthesis** — Combine ideas into new structures
- **Evaluation** — Judge and critique evidence

---

## 🤖 AI Model

### Model Specification

| Property | Value |
|----------|-------|
| **Provider** | Groq Cloud |
| **Model** | `llama-3.1-8b-instant` |
| **Type** | Open-source LLM (Meta Llama) |
| **Parameters** | 8 billion |
| **Context** | 8,192 tokens |
| **Latency** | < 100ms (Groq GroqCloud) |
| **Cost** | Pay-per-token (affordable for education) |

### Why This Model?

✅ **Fast** — Groq's specialized inference engine  
✅ **Reliable** — Proven track record in education  
✅ **Cost-Effective** — Good performance per token  
✅ **Stable** — Open-source, no deprecation risk  
✅ **Capable** — Handles complex curriculum generation  

### What It Generates

1. **Learning Objectives** — Clear, measurable goals using Bloom's taxonomy
2. **Lesson Content** — Comprehensive instructional materials
3. **Assessments** — Quizzes and evaluation questions
4. **Refined Content** — Improved versions on request
5. **Change Summaries** — Explains version differences

### Robustness Features

- **3 Automatic Retries** — Exponential backoff on failure
- **Markdown Unwrapping** — Handles code-block wrapped responses
- **JSON Validation** — Ensures proper structure
- **Graceful Errors** — User-friendly error messages

---

## 🐛 Troubleshooting

### KeyError in Editor

**Error**: `KeyError: 'section_id'` when loading modules

**Solution**:
```powershell
# Stop all Python processes
Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force

# Clear stale data
Remove-Item "AI Copilot_Human-in-the-Loop/modules.db"

# Restart app
streamlit run "AI Copilot_Human-in-the-Loop/app.py"
```

**Cause**: Stale session state or database corruption

---

### Groq API Errors

**Error**: `GROQ_API_KEY not found` or authentication failures

**Solution**:
1. Verify `.env` file exists in project root
2. Check `GROQ_API_KEY=your_key` (no quotes, no spaces)
3. Validate key at https://console.groq.com/keys
4. Restart Streamlit app

**Common Causes**:
- Missing or invalid API key
- `.env` file in wrong directory
- Typo in environment variable name

---

### Invalid JSON Response

**Error**: `JSONDecodeError` or malformed module structure

**Solution**:
- App automatically retries (3 attempts)
- Check internet connection
- Verify Groq status: https://status.groq.com
- Try regenerating the module

**Cause**: Network issues or temporary API errors

---

### Port Already in Use

**Error**: `Port 8501 already in use`

**Solution**:
```powershell
# Option 1: Use different port
streamlit run "AI Copilot_Human-in-the-Loop/app.py" --server.port=8502

# Option 2: Kill existing process
Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force
```

---

### Database Lock

**Error**: `database is locked`

**Solution**:
```powershell
# Stop all Python processes
Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force

# Wait briefly
Start-Sleep -Seconds 2

# Restart app
streamlit run "AI Copilot_Human-in-the-Loop/app.py"
```

---

## 🤝 Contributing

### How to Contribute

**Reporting Issues**
```
Describe the problem clearly
Include steps to reproduce
Show expected vs actual behavior
Provide Python version and environment details
```

**Submitting Code**
```powershell
# Fork and clone
git clone https://github.com/yourusername/ai-copilot.git
cd ai-copilot

# Create feature branch
git checkout -b feature/your-feature-name

# Make changes (PEP 8 style)
# Test thoroughly

# Commit and push
git add .
git commit -m "Clear description of changes"
git push origin feature/your-feature-name

# Submit pull request
```

### Contribution Areas

- 🐛 **Bug Fixes** — Report and fix issues
- 🎯 **Features** — PostgreSQL/MySQL, multi-user auth, RBAC, batch generation, templates
- ✅ **Testing** — Unit tests for `database.py` and `file_utils.py`
- 📖 **Documentation** — README, API docs, tutorials
- 🎨 **UI/UX** — Streamlit interface improvements

### Code Standards

- Follow PEP 8 style guide
- Use type hints where possible
- Add docstrings for functions
- Include comments for complex logic
- Test all changes before submitting
- Update README for new features

---

## 📜 License

**MIT License** — Free for personal and commercial use

You can:
- ✅ Use in personal projects
- ✅ Use commercially
- ✅ Modify code
- ✅ Distribute
- ✅ Private or public projects

You must:
- ⚠️ Include license text
- ⚠️ State changes made

```
MIT License

Copyright (c) 2025 AI Copilot Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 💬 Support

### Getting Help

1. **Check Troubleshooting** — See section above
2. **Review GitHub Issues** — Browse existing solutions
3. **Create New Issue** — Include: problem description, reproduction steps, Python version

### Contact

- **Email**: contact@aicopilot.example.com
- **Issues**: GitHub Issues tracker
- **Schema Docs**: See `DATABASE.md` for detailed database design

### Community

- Questions? Check existing issues
- Found a bug? Report it with clear steps
- Have a feature idea? Open a discussion
- Want to contribute? See Contributing section

---

## 🔧 Development

### Running Tests

```powershell
& ".\venv\Scripts\Activate.ps1"
python -u "AI Copilot_Human-in-the-Loop\utils\test_db_buttons.py"
```

**Test Coverage**:
- Module save/load
- Section edits and version tracking
- Approval/rejection workflows
- Statistics calculation
- Database integrity

### Resetting Database

```powershell
# Remove database file
Remove-Item "AI Copilot_Human-in-the-Loop/modules.db"

# Restart app (auto-recreates database)
streamlit run "AI Copilot_Human-in-the-Loop/app.py"
```

### Cleanup

Safe files to delete:
```powershell
# Cache files
Remove-Item "AI Copilot_Human-in-the-Loop/utils/__pycache__" -Recurse -Force
Remove-Item ".pytest_cache" -Recurse -Force

# Keep everything else
```

---

## 📚 Resources

- **Groq Docs**: https://console.groq.com/docs
- **Streamlit Docs**: https://docs.streamlit.io
- **SQLite Docs**: https://www.sqlite.org/docs.html
- **Python Docs**: https://docs.python.org/3
- **Database Schema**: See `DATABASE.md`

---

## 🎯 Status

**Version**: 1.0.0  
**Status**: Production Ready ✅  
**Last Updated**: November 14, 2025  
**Python**: 3.10+  
**License**: MIT
