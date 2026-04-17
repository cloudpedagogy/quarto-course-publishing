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

The commands below use a YAML configuration file (e.g. `config/outbreak_ve_demo.yml`).

---

## When to run each command

- Run `build` only when you change the course structure (YAML)  
- Run `import-word` when you update Word content  
- Run `render` to generate the final site  

### Typical workflows

**First time setup**  
build → import-word → render  

**After editing Word content**  
import-word → render  

**After changing structure**  
build → import-word → render  

---

## Step 1 — BUILD (Structure)

Run only when you change the course structure (YAML):

```bash
PYTHONPATH=src python3 -m course_generator.cli build config/outbreak_ve_demo.yml
```

This:
- creates or updates QMD files  
- synchronises navigation  
- preserves existing content  

---

## Step 2 — IMPORT-WORD (Content)

Run after editing Word documents:

```bash
PYTHONPATH=src python3 -m course_generator.cli import-word config/outbreak_ve_demo.yml
```

This:
- converts Word → Markdown (via Pandoc)  
- parses directives  
- injects content into QMD  

---

## Step 3 — RENDER (Publish)

```bash
PYTHONPATH=src python3 -m course_generator.cli render config/outbreak_ve_demo.yml
```

This generates the final course site in:

```
output/outbreak_ve_demo/
```

---

## Content Injection Model

Content is inserted into QMD using:

```html
<!-- IMPORT_START -->
<!-- IMPORT_END -->
```

---

## File Structure

```
config/ → YAML  
imports/ → Word  
course/ → QMD  
output/ → HTML  
resources/ → assets  
```

---

## Key Rules

- Do NOT edit `output/`  
- Do NOT edit imported QMD content  
- Always re-run `import-word` after Word updates  

---

## Summary

Structure in YAML, content in Word, system handles transformation.

```
Design → Write → Import → Render → Publish
```
