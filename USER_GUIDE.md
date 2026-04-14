# Course Author’s Guide: Word-First Publishing Workflow

Welcome! This guide explains how to use the **Quarto Course Publishing System** to build structured, professional course websites.

This system follows a **Word-first, scaffold-driven philosophy**:

- YAML defines the structure (the “bones”)
- Word defines the content (the “flesh”)
- The system transforms both into a complete course

---

## 🧠 1. Overview: The Word-First Model

| Layer | Purpose |
|------|--------|
| YAML (`config/course.yml`) | Defines structure |
| Word (`imports/.../docx/`) | Author content |
| QMD (`course/`) | Generated + injected |
| HTML (`output/`) | Final course |

👉 **You primarily write in Word — not in QMD**

---

## 🚀 2. Core Workflow

```bash
build → import-word → render
```

---

### Step 1: BUILD (Structure)

Run when changing course structure:

```bash
PYTHONPATH=src python3 -m course_generator.cli build config/course.yml
```

This:
- creates/updates `.qmd` files
- syncs navigation
- preserves existing content

---

### Step 2: IMPORT-WORD (Content)

Run after editing Word documents:

```bash
PYTHONPATH=src python3 -m course_generator.cli import-word config/course.yml
```

This:
- converts Word → Markdown
- parses structured interactions
- injects content into QMD

---

### Step 3: RENDER (Publish)

```bash
PYTHONPATH=src python3 -m course_generator.cli render config/course.yml
```

This generates the final website in:

```text
output/{module_id}/
```

---

## ✍️ 3. Writing in Word

### Structured Authoring

Write content using patterns like:

```text
Tabs
Interpretation :: Explanation
Assumptions :: Notes

Quiz
Question :: What is VE?
Option :: A
Option :: B
Answer :: A
```

---

### Supported Interaction Types

- Tabs
- Callout
- Quiz
- Reveal
- SelfCheck
- Definition
- R Code
- Image / File / Table

---

## 📦 4. Using Resources

Place files in:

```text
resources/
  pdf/
  data/
  images/
```

Reference in Word:

```text
File :: resources/pdf/report.pdf
Label :: Download report
```

---

## 🧩 5. YAML Structure

YAML defines:

- Modules
- Sessions
- Sections
- Pages

Example:

```yaml
pages:
  - id: page1
    kind: concept_page
    source_docx: imports/.../docx/file.docx
```

---

## 🔄 6. Content Injection

Content is inserted into QMD using:

```html
<!-- IMPORT_START -->
<!-- IMPORT_END -->
```

This allows:
- safe updates
- repeated imports
- no duplication

---

## ⚠️ 7. Key Rules

- Do NOT edit `output/`
- Do NOT manually edit imported content
- Always rerun `import-word` after Word changes
- Keep Word formatting simple

---

## 🩺 8. Troubleshooting

### Broken links
- Check `resources/`
- Re-run import + render

### R code errors
- Caused by formatting → auto-fixed in import

### Missing content
- Check `.bak` files

---

## 🎯 Final Tip

Think of the system as:

```text
Design → Write → Transform → Publish
```

Not:

```text
Edit HTML directly
```

---

**Happy authoring — your structure is stable, and your content is safe.**
