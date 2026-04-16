# 🚀 Quick Start Guide (Word-First Workflow)

## Purpose

This guide explains the workflow for building a course using YAML and Word.

> For a copy-paste setup, see README.md

---

## What You Will Do

1. Define structure in YAML  
2. Write content in Word  
3. Run three commands:
   build → import-word → render  
4. Open your course website  

---

## Prerequisites

→ See PREREQUISITES.md

---

## Step 1 — Define Structure (YAML)

Edit:

```
config/course.yml
```

Example:

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

## Step 2 — Add Word Content

Create:

```
imports/demo_course/docx/
```

Add `welcome.docx` with content like:

```
Callout :: note
Text :: Welcome to the course.

Quiz
Question :: What is 2 + 2?
Option :: 3
Option :: 4
Answer :: 4
```

---

## Step 3 — Build

```bash
PYTHONPATH=src python3 -m course_generator.cli build config/course.yml
```

---

## Step 4 — Import Word

```bash
PYTHONPATH=src python3 -m course_generator.cli import-word config/course.yml
```

---

## Step 5 — Render

```bash
PYTHONPATH=src python3 -m course_generator.cli render config/course.yml
```

---

## Step 6 — View

Open:

```
output/demo_course/index.html
```

---

## When to Run Each Step

- build → when YAML structure changes  
- import-word → when Word content changes  
- render → to generate or refresh the site  

---

## Key Rules

- Do NOT edit `output/`
- Always edit YAML or Word
- Re-run import-word after Word changes

---

## Workflow Summary

```
Structure → build
Content → import-word
Publish → render
```

---

## If Something Goes Wrong

- Re-run import-word and render  
- Check YAML paths  
- Check Word directive syntax (::)

---

## Summary

> YAML defines structure, Word defines content, system generates the course.
