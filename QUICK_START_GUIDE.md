# 🚀 Quick Start Guide

This guide helps you get up and running with the **Quarto Course Publishing System** in minutes.

---

## 🧠 What You Are Doing

You will:

1. Define a course structure in YAML
2. Add content in Word documents
3. Run three commands:
   ```
   build → import-word → render
   ```
4. Open your generated course website

---

## ⚙️ Prerequisites

Make sure you have installed:

- Python 3.10+
- Quarto CLI (`quarto --version`)
- Pandoc (`pandoc --version`)

Install Python dependencies:

```bash
pip install -r requirements.txt
pip install -e .
```

---

## 📁 Step 1 — Create Course Structure (YAML)

Edit or create:

```
config/course.yml
```

Minimal example:

```yaml
module:
  id: demo_course
  title: Demo Course

sessions:
  - id: se01
    title: Introduction
    sections:
      - id: sec01
        title: Getting Started
        pages:
          - id: page01
            title: Welcome
            kind: concept_page
            source_docx: imports/demo_course/docx/welcome.docx
```

---

## 📄 Step 2 — Add Word Content

Create folder:

```
imports/demo_course/docx/
```

Add a Word file:

```
welcome.docx
```

Example content inside Word:

```
Callout :: important
Text :: This is an important concept.

Tabs
Overview :: This is the overview.
Details :: This is more detail.

Quiz
Question :: What is 2 + 2?
Option :: 3
Option :: 4
Answer :: 4
```

---

## 🏗️ Step 3 — Build Structure

```bash
PYTHONPATH=src python3 -m course_generator.cli build config/course.yml
```

This creates `.qmd` files in:

```
course/demo_course/
```

---

## 📥 Step 4 — Import Word Content

```bash
PYTHONPATH=src python3 -m course_generator.cli import-word config/course.yml
```

This:
- converts Word → Markdown
- parses interactions
- injects content into QMD files

---

## 🌐 Step 5 — Render Website

```bash
PYTHONPATH=src python3 -m course_generator.cli render config/course.yml
```

Output is generated in:

```
output/demo_course/
```

---

## 👀 Step 6 — View Your Course

Open:

```
output/demo_course/index.html
```

---

## 📦 Adding Resources (Optional)

Place files in:

```
resources/pdf/
resources/data/
resources/images/
```

Use in Word:

```
File :: resources/pdf/example.pdf
Label :: Download file
```

---

## ⚠️ Key Rules

- Do NOT edit `output/`
- Always edit Word or YAML
- Always re-run `import-word` after Word changes

---

## 🧩 Workflow Summary

```
Edit YAML → build
Edit Word → import-word
Render → view site
```

---

## 🧠 If Something Goes Wrong

- Re-run `import-word`
- Re-run `render`
- Check Word formatting
- Check YAML structure

---

## ✅ You’re Ready

You now have a fully working pipeline:

👉 YAML + Word → Quarto → Website

Happy building!
