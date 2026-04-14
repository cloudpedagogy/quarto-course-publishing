# Quarto Course Generator

A **Word-first, YAML-structured publishing system** for generating flexible, pedagogically structured course websites and materials from configuration files.

The system combines structured curriculum design (YAML) with accessible content authoring (Word), producing fully rendered, interactive HTML course sites via Quarto.

> [!IMPORTANT]
> **Authoritative Guides**: 
> - [QUICK_START_GUIDE.md](QUICK_START_GUIDE.md): Get up and running in minutes (recommended starting point)
> - [INSTRUCTIONS.md](INSTRUCTIONS.md): Operational guide for setup, authoring, and publishing.
> - [USER_GUIDE.md](USER_GUIDE.md): Master workflow guide for course authors.
> - [PROJECT_SPEC.md](PROJECT_SPEC.md): Technical specification and architectural deep-dive.

---

## 🧠 System Overview

This system follows a **separation of concerns model**:

- **YAML (`config/`) → Structure**
  - Defines modules, sessions, sections, pages
  - Controls pedagogy, sequencing, and layout

- **Word (`.docx`) → Content**
  - Academics author content in structured Word documents
  - Includes interactions (Tabs, Quiz, Callout, etc.)

- **Import Layer (`import_word.py`) → Transformation**
  - Converts Word → Markdown (via Pandoc)
  - Parses structured interaction patterns
  - Injects content into `.qmd` files (idempotent)

- **Quarto → Rendering**
  - Generates final HTML course website

---

## 🚀 Quick Start (First Run)

1. Define your course in `config/course.yml`
2. Add Word files to:
   ```
   imports/{course_id}/docx/
   ```
3. Link them in YAML:
   ```yaml
   source_docx: imports/{course_id}/docx/your_file.docx
   ```
4. Run:
   ```bash
   PYTHONPATH=src python3 -m course_generator.cli build config/course.yml
   PYTHONPATH=src python3 -m course_generator.cli import-word config/course.yml
   PYTHONPATH=src python3 -m course_generator.cli render config/course.yml
   ```
5. Open:
   ```
   output/{course_id}/index.html
   ```

---

## 🔁 Core Workflow

```bash
build → import-word → render
```

### 1. Build a Course (Structure)
```bash
PYTHONPATH=src python3 -m course_generator.cli build config/course.yml
```

### 2. Import Word Content
```bash
PYTHONPATH=src python3 -m course_generator.cli import-word config/course.yml
```

### 3. Render Site
```bash
PYTHONPATH=src python3 -m course_generator.cli render config/course.yml
```

### Optional: Preview a Page
```bash
PYTHONPATH=src python3 -m course_generator.cli preview config/course.yml --path path/to/page.qmd
```

---

## ✨ Features

- **Hierarchical Structure**  
  Organise courses using **Module → Session → Section → Page**

- **Smart Interaction Sync**  
  Safely edit pedagogical blocks without losing content during rebuilds

- **Pedagogical Interaction Kit**  
  Built-in interactions including quizzes, self-checks, callouts, tabs, and more

- **Variant System**  
  Control styles (e.g., `warning` vs `tip`) via YAML flags

- **Word → Interaction Parsing Layer**  
  Structured content in Word (e.g. `Tabs`, `Quiz`, `Callout`) is automatically parsed into Quarto-compatible formats

- **Resource Propagation System**  
  Static assets (PDFs, datasets, images) are automatically copied and made available across course and output layers

---

## 📁 Project Structure

```
.
├── config/                      # YAML course blueprints
├── course/{module_id}/          # QMD authoring layer (generated + injected content)
├── imports/{module_id}/docx/    # Source Word documents
├── imports/{module_id}/md/      # Intermediate Markdown (Pandoc output)
├── resources/                   # Global static assets
├── output/{module_id}/          # Rendered Quarto site
├── templates/                   # Jinja2 templates
├── docs/                        # Internal interaction documentation
├── src/                         # Core Python logic
```

---

## 🔄 Content Pipeline (Word → Course)

```
Word (.docx)
   ↓
Pandoc → Markdown (imports/md/)
   ↓
Interaction Parsing (import_word.py)
   ↓
Injection into QMD (course/)
   ↓
Quarto Render → HTML (output/)
```

Key characteristics:

- **Idempotent**: Content safely re-imported using markers  
- **Transparent**: Intermediate Markdown preserved for debugging  
- **Non-destructive**: Existing content not overwritten  

---

## 📦 Resource Handling

Place assets in:

```
resources/
  pdf/
  data/
  images/
```

Example (Word):

```
File :: resources/pdf/outbreak-report.pdf
Label :: Download report
```

Resources are automatically copied and linked appropriately for nested pages.

---

## ⚠️ Key Rules

- Do not edit `output/`
- Always edit Word or YAML
- Always rerun import after Word changes

---

## Word Content Import (Core System)

### Usage
```bash
PYTHONPATH=src python3 -m course_generator.cli import-word config/course.yml
```

### Features
- **Idempotent**: Uses `<!-- IMPORT_START -->` markers to safely replace content
- **Safe**: Creates `.bak` backups of modified QMD files
- **Conversion**: Uses Pandoc for DOCX → Markdown
- **Interaction Parsing**: Converts structured patterns into Quarto components
- **R Code Support**: Detects and renders `{r}` code blocks correctly

---

## Status

This project is an evolving system developed through applied work in higher education course design and publishing workflows.

---

## Use and Adaptation

This repository is made available for educational and non-commercial exploration.

---

## Attribution

Developed by Jonathan Wong as part of ongoing work in structured curriculum design and course publishing systems in higher education.

---

## Important Note on Context

This system has been developed through applied work in higher education environments. Users are responsible for appropriate adaptation and use within their own institutional context.

---

## Disclaimer

This project is provided "as is" without warranty. It is intended for experimentation and development rather than production-supported deployment.
