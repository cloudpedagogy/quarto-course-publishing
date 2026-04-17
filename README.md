# Quarto Course Publishing System

A Word-first, YAML-structured publishing system for generating pedagogically structured course websites using Quarto.

The system combines:
- YAML for curriculum structure
- Word for content authoring
- Quarto for final rendering

---

## Start Here

Choose your path:

### I want to create course content
→ [Author Pack](docs/author_pack/quarto_authoring_pack.md)

### I want to get something running quickly
→ [Quick Start Guide](QUICK_START_GUIDE.md)

### I want to run the system (build, import, render)
→ [Running the System](RUNNING_THE_SYSTEM.md)

### I want to understand the system design
→ [Project Specification](PROJECT_SPEC.md)

### I need to install dependencies
→ [Prerequisites](PREREQUISITES.md)

---

## ⚡ Quick Setup (Copy & Run)

Follow these steps to get the system running from scratch.

> Run all commands from the project root folder (where `config/` and `src/` are located).

---

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd <your-repo-folder>
```

---

### 2. Set up Python environment (Recommended)

It is recommended to use a virtual environment to avoid affecting your system Python.

See [PREREQUISITES.md](PREREQUISITES.md) for full details.

#### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

#### Windows (Command Prompt)

```cmd
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

---

#### Windows (PowerShell)

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

---

### 3. Check required tools

```bash
python --version
pandoc --version
quarto --version
```

If anything is missing, see:
→ [PREREQUISITES.md](PREREQUISITES.md)

---

### 4. Run the pipeline

#### macOS / Linux

```bash
PYTHONPATH=src python3 -m course_generator.cli build config/course.yml
PYTHONPATH=src python3 -m course_generator.cli import-word config/course.yml
PYTHONPATH=src python3 -m course_generator.cli render config/course.yml
```

---

#### Windows (Command Prompt)

```cmd
set PYTHONPATH=src
python -m course_generator.cli build config/course.yml
python -m course_generator.cli import-word config/course.yml
python -m course_generator.cli render config/course.yml
```

---

#### Windows (PowerShell)

```powershell
$env:PYTHONPATH="src"
python -m course_generator.cli build config/course.yml
python -m course_generator.cli import-word config/course.yml
python -m course_generator.cli render config/course.yml
```

---

### 5. Open your course

```
output/<course_id>/index.html
```

---

## System Overview

This system follows a clear separation of concerns:

| Layer | Role |
|------|------|
| YAML (`config/`) | Defines structure |
| Word (`imports/.../docx/`) | Defines content |
| QMD (`course/`) | Generated container |
| HTML (`output/`) | Final course |

---

## Core Workflow

```bash
build → import-word → render
```

- build → create/update structure  
- import-word → inject content  
- render → generate website  

---

## Interaction System

Content authored in Word supports structured interactions:

- Callout  
- Tabs  
- Quiz (formative, no scoring)  
- Reveal  
- SelfCheck  
- R Code  
- Image / File / Table  

These are parsed and rendered automatically.

---

## Project Structure

```text
config/        → YAML structure
imports/       → Word + Markdown
course/        → generated QMD
output/        → final site
resources/     → assets
templates/     → layouts
src/           → system logic
docs/          → user-facing guides
```

---

## Content Pipeline

```text
Word (.docx)
   ↓
Pandoc → Markdown
   ↓
Directive Parsing
   ↓
Injection into QMD
   ↓
Quarto Render → HTML
```

---

## Key Rules

- Do NOT edit `output/`
- Edit only YAML or Word
- Always rerun `import-word` after content changes

---

## Design Philosophy

- Word = semantic intent
- YAML = structure
- Python = transformation
- Quarto = presentation
