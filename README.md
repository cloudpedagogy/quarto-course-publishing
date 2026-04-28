# Quarto Course Publishing System

A Word-first, YAML-structured publishing system for generating pedagogically structured course websites using Quarto.

The system combines:
- YAML for curriculum structure  
- Word for content authoring  
- Quarto for final rendering  

---

## Start Here

Choose your path:

### I want to create course content  
→ [Author Pack](docs/author_pack/quarto_authoring_pack.md)

### I want to get something running quickly  
→ [Quick Start Guide](QUICK_START_GUIDE.md)

### I want to run the system (build, import, render)  
→ [Running the System](RUNNING_THE_SYSTEM.md)

### I want to understand the system design  
→ [Project Specification](PROJECT_SPEC.md)

### I need to install dependencies  
→ [Prerequisites](PREREQUISITES.md)

---

## Quick Setup (Copy and Run)

Follow these steps to get the system running from scratch.

Run all commands from the project root folder (where `config/` and `src/` are located).

---

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd <your-repo-folder>
```

---

### 2. Set up Python environment (recommended)

It is recommended to use a virtual environment to avoid affecting your system Python.

See [PREREQUISITES.md](PREREQUISITES.md) for full details.

#### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

#### Windows (Command Prompt)

```cmd
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

#### Windows (PowerShell)

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

---

### 3. Check required tools

```bash
python --version
pandoc --version
quarto --version
```

If anything is missing, see:
→ [PREREQUISITES.md](PREREQUISITES.md)

---

### 4. Run the pipeline

For the demo, use the configuration file:

`config/outbreak_ve_demo.yml`

#### macOS / Linux

```bash
PYTHONPATH=src python3 -m course_generator.cli build config/outbreak_ve_demo.yml
PYTHONPATH=src python3 -m course_generator.cli import-word config/outbreak_ve_demo.yml
PYTHONPATH=src python3 -m course_generator.cli render config/outbreak_ve_demo.yml
```

#### Windows (Command Prompt)

```cmd
set PYTHONPATH=src && python -m course_generator.cli build config/outbreak_ve_demo.yml
set PYTHONPATH=src && python -m course_generator.cli import-word config/outbreak_ve_demo.yml
set PYTHONPATH=src && python -m course_generator.cli render config/outbreak_ve_demo.yml
```

#### Windows (PowerShell)

```powershell
$env:PYTHONPATH="src"
python -m course_generator.cli build config/outbreak_ve_demo.yml
python -m course_generator.cli import-word config/outbreak_ve_demo.yml
python -m course_generator.cli render config/outbreak_ve_demo.yml
```

---

### 5. Open your course

```
output/outbreak_ve_demo/index.html
```

---

## System Overview

This system follows a clear separation of concerns:

| Layer | Role |
|------|------|
| YAML (`config/`) | Defines structure |
| Word (`imports/.../docx/`) | Defines content |
| QMD (`course/`) | Generated container |
| HTML (`output/`) | Final course |

---

## Core Workflow

```bash
build → import-word → render
```

- build → create or update structure  
- import-word → inject content  
- render → generate website  

The commands use a YAML configuration file (e.g. `config/outbreak_ve_demo.yml`).

### Typical usage

- First run:  
  build → import-word → render  

- After editing Word:  
  import-word → render  

- After changing structure:  
  build → import-word → render  

---

## Interaction System

Content authored in Word supports structured interactions:

- Callout  
- Tabs  
- Quiz (formative, no scoring)  
- Reveal  
- SelfCheck  
- R Code  
- Image / File / Table  

These are parsed and rendered automatically.

---

## Project Structure

```text
config/        → YAML structure  
imports/       → Word + Markdown  
course/        → generated QMD  
output/        → final site  
resources/     → assets  
templates/     → layouts  
src/           → system logic  
docs/          → user-facing guides  
```

---

## Content Pipeline

```text
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

---

## Key Rules

- Do NOT edit `output/`  
- Edit only YAML or Word  
- Always rerun `import-word` after content changes  

---

## Authoring R Code from Word

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

## Important Authoring Rules

- Always close blocks with `END R Code` or `END R Example`
- Block names should be written as:
  - `R Code`
  - `END R Code`
  - `R Example`
  - `END R Example`
- Avoid using these phrases in normal text unless formatted as headers or code blocks

---

## Common Errors

**Example error:**
`"attempt to use zero-length variable name"`

**Cause:**
- R Code block not properly closed
- Parser incorrectly includes non-code text

**Fix:**
- Ensure `END R Code` or `END R Example` is present
- Re-run `import-word`, then `render`

---

## Accessibility Notes

- R charts support `Alt ::` (screen reader description)
- `Caption ::` provides visible figure labels
- YouTube embeds include title attributes
- Panopto embeds include title attributes
- PDF embeds include iframe title using `Label ::`

---

## Tables from Word

- Use:
  `Table: Summary of outbreak cases`
- Pandoc converts this into a proper caption
- Manual numbering (e.g. Table 1) is optional

---

## Design Philosophy

- Word = semantic intent  
- YAML = structure  
- Python = transformation  
- Quarto = presentation  
