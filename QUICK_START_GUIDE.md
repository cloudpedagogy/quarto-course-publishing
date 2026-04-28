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

## Advanced Authoring (R Code, Tables, Accessibility)

### Authoring R Code from Word

Explain two supported patterns:

#### Executable R Code (runs during Quarto render)

```text
R Code
Alt :: Bar chart showing risk of infection for vaccinated and unvaccinated groups.
Caption :: Risk of Infection by Vaccination Status

group <- c("Vaccinated", "Unvaccinated")
cases <- c(5, 25)
population <- c(500, 500)
risk <- cases / population
barplot(risk, names.arg = group, col = c("steelblue", "tomato"),
main = "Risk of Infection by Vaccination Status")

END R Code
```

Explanation:
- This block is executed by Quarto
- It can generate charts, tables, or printed output
- `Alt ::` is used for accessibility (screen readers)
- `Caption ::` is the visible figure caption
- `END R Code` is required to close the block

#### Display-only R Example (not executed)

```text
R Example
group <- c("Vaccinated", "Unvaccinated")
cases <- c(5, 25)
population <- c(500, 500)

risk <- cases / population
risk

END R Example
```

Explanation:
- This block is NOT executed
- It is rendered as formatted code only
- No charts or output are generated
- Useful for teaching, explanation, or comparison
- `END R Example` is required

---

### Important Authoring Rules

- Always close blocks with `END R Code` or `END R Example`
- Block names should be written as:
  - `R Code`
  - `END R Code`
  - `R Example`
  - `END R Example`
- Avoid using these phrases in normal text unless formatted as headers or code blocks

---

### Common Errors

**Example error:**
`"attempt to use zero-length variable name"`

**Cause:**
- R Code block not properly closed
- Parser incorrectly includes non-code text

**Fix:**
- Ensure `END R Code` or `END R Example` is present
- Re-run `import-word`, then `render`

---

### Accessibility Notes

- R charts support `Alt ::` (screen reader description)
- `Caption ::` provides visible figure labels
- YouTube embeds include title attributes
- Panopto embeds include title attributes
- PDF embeds include iframe title using `Label ::`

---

### Tables from Word

- Use:
  `Table: Summary of outbreak cases`
- Pandoc converts this into a proper caption
- Manual numbering (e.g. Table 1) is optional

---

## Summary

> YAML defines structure, Word defines content, system generates the course.
