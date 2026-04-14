# Operational Instructions: Quarto Course Publishing

This guide provides step-by-step instructions for setting up, authoring, and publishing courses using the system.

---

## 🚀 0. Quick Start (First Run)

Follow this sequence for a new course:

1. Define structure in `config/course.yml`
2. Add Word files to:
   ```
   imports/{course_id}/docx/
   ```
3. Link Word files in YAML using `source_docx`
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

## 1. Environment Setup

### 1.1 Prerequisites

- **Python 3.10+**
- **Quarto CLI (v1.3+)**
- **Pandoc** (required for Word import)

### 1.2 Installation

```bash
git clone <remote-url>
cd lshtm-quarto-publishing

pip install -r requirements.txt
pip install -e .
```

---

## 2. Core Workflow

```bash
build → import-word → render
```

---

### 2.1 BUILD (Structure Phase)

```bash
PYTHONPATH=src python3 -m course_generator.cli build config/course.yml
```

- Generates QMD scaffolds
- Syncs structure
- Preserves content

---

### 2.2 IMPORT-WORD (Content Phase)

```bash
PYTHONPATH=src python3 -m course_generator.cli import-word config/course.yml
```

- Converts DOCX → Markdown
- Parses interactions
- Injects into QMD

---

### 2.3 RENDER (Publishing Phase)

```bash
PYTHONPATH=src python3 -m course_generator.cli render config/course.yml
```

Output:
```
output/{module_id}/
```

---

### Optional: PREVIEW

```bash
PYTHONPATH=src python3 -m course_generator.cli preview config/course.yml --path path/to/page.qmd
```

---

## 3. Authoring Model

### 3.1 Where to Write

| Layer | Responsibility |
|------|----------------|
| YAML | Structure |
| Word | Content |
| QMD | Generated |

---

### 3.2 Linking Word Files (Important)

In YAML:

```yaml
source_docx: imports/{course_id}/docx/file.docx
```

---

### 3.3 Word Authoring

```text
Tabs
Interpretation :: ...

Quiz
Question :: ...
Answer :: ...
```

---

### 3.4 Import Markers

```html
<!-- IMPORT_START -->
<!-- IMPORT_END -->
```

---

## 4. Resource Handling

### Structure

```
resources/
  pdf/
  data/
  images/
```

### Usage

```text
File :: resources/pdf/file.pdf
Label :: Download file
```

### Behaviour

- Copied into course + output
- Paths rewritten automatically

---

## 5. Recovery & Safety

If something breaks:

- Delete `output/` → rerun render
- Re-run `import-word`
- Check `.bak` files
- Check `imports/md/`

---

## 6. Troubleshooting

### Broken links
- Check resources exist
- Re-run import + render

### R errors
- Caused by escaping
- Auto-fixed during import

### YAML errors
- Check indentation

---

## 7. Key Rules

- Do NOT edit `output/`
- Always re-run import after Word changes
- Keep Word simple

---

## 8. System Requirements Check (Recommended)

Ensure tools are available:

```bash
quarto --version
pandoc --version
```

---

**End of Operational Guide**
