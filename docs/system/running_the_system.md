# Running the Quarto Course Publishing System

> ⚠️ This guide explains how to **run the system** (build, import, render).
>
> If you are writing course content, start here instead:
> → Author Pack (Word-Based Authoring Guide)

---

## Purpose

This guide explains how to execute the Quarto Course Publishing System after your course structure (YAML) and content (Word) are prepared.

It focuses on **running and managing the system**, not writing content.

---

## System Model (Quick Reference)

- YAML → structure
- Word → content
- QMD → generated container
- HTML → final output

---

## Core Workflow

```bash
build → import-word → render
```

---

## Step 1 — BUILD (Structure)

Run when you change course structure:

```bash
PYTHONPATH=src python3 -m course_generator.cli build config/course.yml
```

This:
- creates or updates QMD files
- synchronises navigation
- preserves existing content

---

## Step 2 — IMPORT-WORD (Content)

Run after editing Word documents:

```bash
PYTHONPATH=src python3 -m course_generator.cli import-word config/course.yml
```

This:
- converts Word → Markdown (via Pandoc)
- parses directives (Quiz, Tabs, etc.)
- injects content into QMD between markers

---

## Step 3 — RENDER (Publish)

```bash
PYTHONPATH=src python3 -m course_generator.cli render config/course.yml
```

This generates the final course site in:

```
output/{course_id}/
```

---

## Content Injection Model

Content is inserted into QMD using:

```html
<!-- IMPORT_START -->
<!-- IMPORT_END -->
```

This ensures:
- safe updates
- idempotent imports
- no duplication

---

## File Structure (Key Locations)

```
config/          → course structure (YAML)
imports/         → Word documents
course/          → generated QMD files
output/          → final HTML output
resources/       → images, PDFs, etc.
```

---

## Key Rules

- Do NOT edit files in `output/`
- Do NOT manually edit imported content inside QMD
- Always re-run `import-word` after updating Word files
- Keep Word formatting simple

---

## Using Resources

Store files in:

```
resources/
  images/
  pdf/
  data/
```

Reference in Word using:

```
File :: resources/pdf/example.pdf
Label :: Download file
```

---

## Troubleshooting

### Missing or incorrect content
- Re-run: build → import-word → render

### Broken links or missing files
- Check `resources/` paths
- Ensure files exist

### Import warnings
- Check terminal output
- Look for directive syntax issues (use `::` not `:`)

---

## Clean Rebuild (if needed)

```bash
rm -rf course/<course_id>
rm -rf output/<course_id>

PYTHONPATH=src python3 -m course_generator.cli build config/course.yml
PYTHONPATH=src python3 -m course_generator.cli import-word config/course.yml
PYTHONPATH=src python3 -m course_generator.cli render config/course.yml
```

---

## Summary

> Structure in YAML, content in Word, system handles transformation.

Your role here is to:
- run the pipeline
- verify outputs
- troubleshoot when needed

---

## Final Note

Think of this as a **publishing pipeline**, not an editing environment:

```
Design → Write → Import → Render → Publish
```
