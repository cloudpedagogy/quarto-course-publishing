# Project Specification: Quarto Course Publishing System

## 1. Executive Summary

The Quarto Course Publishing System is a **Word-first, YAML-structured publishing engine** designed to generate structured, pedagogically rich course websites using Quarto.

The system follows a dual-authoring model:

- **YAML defines structure**
- **Word defines content**

Content authored in Microsoft Word is transformed via Pandoc into Markdown, parsed into structured interactions, and injected into Quarto (`.qmd`) files before final rendering.

This enables scalable, consistent, and non-destructive course production.

---

## 2. Technical Stack

- **Languages**: Python 3.10+
- **Markup**: Quarto (.qmd), Markdown (GFM)
- **Templating**: Jinja2
- **Data Validation**: Pydantic
- **CLI Framework**: Click
- **External Tools**:
  - Pandoc (DOCX → Markdown conversion)
  - Quarto (rendering engine)
- **Infrastructure**: Git (version control and collaboration)

---

## 3. Core Architecture

### 3.1 Hierarchy Model

The system follows a strict pedagogical hierarchy:

1. **Module** — Top-level course container  
2. **Session** — High-level grouping (e.g. week or theme)  
3. **Section** — Unit of learning  
4. **Page** — Atomic learning object  

---

### 3.2 System Components

- **Generator**
  - Builds course structure from YAML
  - Manages navigation and file sync

- **InteractionResolver**
  - Renders interaction templates (YAML-driven)

- **PageKindResolver**
  - Applies layout templates

- **TemplateManager**
  - Handles Jinja2 rendering

- **WordImporter (`import_word.py`)**
  - Converts DOCX → Markdown via Pandoc
  - Parses structured interaction syntax
  - Injects content into QMD files

---

### 3.3 Content Transformation Pipeline

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

Key properties:

- **Idempotent** — safe repeated imports
- **Non-destructive** — preserves authored content
- **Transparent** — intermediate Markdown retained

---

## 4. Key Features

### 4.1 Non-Destructive Sync

Uses markers:

```
<!-- IMPORT_START -->
<!-- IMPORT_END -->
```

to safely replace imported content without duplication.

---

### 4.2 Word-Based Authoring

Content is authored in Word using structured patterns:

- Tabs  
- Quiz  
- Callout  
- Reveal  
- SelfCheck  

These are parsed into Quarto-compatible structures.

---

### 4.3 Dual Interaction System

- YAML-defined interactions (template-driven)
- Word-parsed interactions (content-driven)

---

### 4.4 Resource Propagation

Static assets are managed across:

- global `resources/`
- course-level `resources/`
- output-level `resources/`

Files are copied and linked automatically.

---

### 4.5 Pedagogical Interaction Kit

Supports 20+ interaction types including:

- Assessment (quiz, self-check)
- Engagement (tabs, reveal)
- Information design (callouts, tables)

---

## 5. Data Schema (YAML)

Validated using Pydantic.

Key fields:

- `id` — unique identifier  
- `kind` — page template  
- `interactions` — pedagogical blocks  
- `source_docx` — Word source file  
- `render_mode` — output mode  

---

## 6. Project Structure

```
.
├── config/                      # YAML course definitions
├── course/                      # QMD authoring layer
├── imports/
│   ├── docx/                   # Word sources
│   └── md/                     # Intermediate Markdown
├── resources/                  # Static assets
├── output/                     # Rendered site
├── docs/                       # Internal docs
├── src/                        # Core logic
├── templates/                  # Jinja templates
├── tests/                      # Tests
└── PROJECT_SPEC.md
```

---

## 7. Design Principles

- **Separation of concerns** (structure vs content)
- **Idempotency** (safe reprocessing)
- **Transparency** (visible intermediate steps)
- **Extensibility** (modular interactions)
- **Local-first** (no backend dependency)

---

## 8. Output

Final output is a static Quarto-generated HTML site:

- Fully navigable
- Resource-linked
- Interaction-enabled

---

## 9. Summary

The system is not just a generator, but a **structured publishing pipeline** that transforms:

→ Curriculum design (YAML)  
→ Authored content (Word)  
→ Interactive course delivery (Quarto)

into a unified, scalable workflow.
