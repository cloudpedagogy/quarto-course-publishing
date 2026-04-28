# Project Specification: Quarto Course Publishing System (Updated)

## 1. Executive Summary

The Quarto Course Publishing System is a **Word-first, YAML-structured publishing engine** for generating structured, pedagogically rich course websites.

The system now follows a **clear primary model**:

- **YAML defines structure (authoritative)**
- **Word defines content (primary authoring interface)**
- **QMD acts as an internal render container**
- **Quarto produces the final HTML output**

> Direct QMD editing is supported only as an advanced fallback, not a primary workflow.

---

## 2. Technical Stack

- **Languages**: Python 3.10+
- **Markup**: Quarto (.qmd), Markdown
- **Templating**: Jinja2
- **Validation**: Pydantic
- **CLI**: Click
- **External Tools**:
  - Pandoc (DOCX → Markdown)
  - Quarto (rendering)
- **Infrastructure**: Git

---

## 3. Core Architecture

### 3.1 Hierarchy Model

The system follows a pedagogical hierarchy:

1. Module  
2. Session  
3. Section  
4. Page  

Each **page is the atomic learning unit**.

---

### 3.2 System Components

- **Generator**
  - Builds structure from YAML
  - Syncs navigation and QMD files

- **PageKindResolver**
  - Applies page scaffolds (`templates/pages/*.qmd`)

- **TemplateManager**
  - Handles layout templates (`.qmd.j2`)

- **WordImporter (`import_word.py`)**
  - Converts DOCX → Markdown (Pandoc)
  - Parses Word directives
  - Injects content into QMD

---

### 3.3 Content Transformation Pipeline

```
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

Key properties:

- **Idempotent** (safe re-import)
- **Non-destructive**
- **Word-first authoring**

---

## 4. Key Features

### 4.1 Word-First Authoring

Content is written in Word using structured directives:

- Callout  
- Quiz  
- Tabs  
- Reveal  
- SelfCheck  
- Media (Image, File, Video)

---

### 4.2 Directive-Based Interaction System

Interactions are defined in Word using:

```
Directive :: value
```

These are parsed into structured Quarto output.

> YAML-based interaction definitions are now deprecated for end users and retained only as internal design references.

---

### 4.3 Idempotent Content Injection

Uses markers:

```
<!-- IMPORT_START -->
<!-- IMPORT_END -->
```

Ensures:
- safe updates
- no duplication
- repeatable imports

---

### 4.4 Template System

Two layers:

- **Wrapper templates** (`.qmd.j2`) → layout and navigation
- **Page scaffolds** (`templates/pages/*.qmd`) → content structure

---

### 4.5 Resource Management

Assets are stored in:

```
resources/
  images/
  pdf/
  data/
```

Automatically copied and linked into output.

---

## 5. Data Schema (YAML)

YAML defines:

- structure (modules, sessions, pages)
- page types (`kind`)
- source Word documents (`source_docx`)

YAML does **not define content or interactions**.

---

## 6. Project Structure

```
config/        → YAML structure
imports/       → Word + Markdown
course/        → generated QMD
output/        → rendered site
resources/     → static assets
templates/     → layouts and scaffolds
src/           → system logic
docs/          → documentation
```

---

## 7. Design Principles

- **Separation of concerns** (structure vs content)
- **Word-first usability**
- **Idempotent processing**
- **Transparency**
- **Local-first execution**
- **Pedagogical alignment**

---

## 8. Output

Produces a static Quarto HTML course:

- structured navigation
- embedded media
- interactive components

---

## 9. Current System Position

The system is best understood as:

> A structured publishing pipeline where:
> - YAML defines curriculum architecture
> - Word defines teaching content
> - The system compiles both into a consistent course

---

## 10. Authoring R Code from Word

Explain two supported patterns:

### Executable R Code (runs during Quarto render)

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

### Display-only R Example (not executed)

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

## 11. Important Authoring Rules

- Always close blocks with `END R Code` or `END R Example`
- Block names should be written as:
  - `R Code`
  - `END R Code`
  - `R Example`
  - `END R Example`
- Avoid using these phrases in normal text unless formatted as headers or code blocks

---

## 12. Common Errors

**Example error:**
`"attempt to use zero-length variable name"`

**Cause:**
- R Code block not properly closed
- Parser incorrectly includes non-code text

**Fix:**
- Ensure `END R Code` or `END R Example` is present
- Re-run `import-word`, then `render`

---

## 13. Accessibility Notes

- R charts support `Alt ::` (screen reader description)
- `Caption ::` provides visible figure labels
- YouTube embeds include title attributes
- Panopto embeds include title attributes
- PDF embeds include iframe title using `Label ::`

---

## 14. Tables from Word

- Use:
  `Table: Summary of outbreak cases`
- Pandoc converts this into a proper caption
- Manual numbering (e.g. Table 1) is optional

---

## 15. Summary

The Quarto Course Publishing System transforms:

→ Curriculum structure (YAML)  
→ Authored content (Word)  
→ Interactive course delivery (Quarto)

into a unified, scalable, and maintainable workflow.

> The primary focus is now **stability, clarity, and institutional usability**, rather than feature expansion.
