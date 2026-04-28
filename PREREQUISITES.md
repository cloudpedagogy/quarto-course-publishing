# PREREQUISITES.md

## ⚙️ System Prerequisites

Before using the Quarto Course Publishing System, ensure the following are installed.

---

## 1. Python and R Environments

### Python Environment
- Python **3.10 or higher**
https://www.python.org/downloads/

### R Environment
- R (required for rendering some content in the demo)
https://cran.r-project.org/

### Check version

**macOS / Linux**
```bash
python3 --version
R --version
```

**Windows**
```cmd
python --version
R --version
```

---

## 2. Install Required R Package

This demo includes some R-based content, which is executed using the Knitr engine.

After installing R, open R (or RStudio) and run:

```R
install.packages("knitr")
```

This only needs to be done once.

---

## 🔒 Recommended: Use a Virtual Environment

It is strongly recommended to run this project inside a virtual environment.

This keeps dependencies isolated and prevents conflicts with other software on your machine.

If anything goes wrong, you can simply delete the `.venv` folder and start again.

---

### Create and activate a virtual environment

#### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

#### Windows (Command Prompt)

```cmd
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

---

#### Windows (PowerShell)

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

---

### Deactivate environment

```bash
deactivate
```

---

## Alternative (Not Recommended)

You can install dependencies globally:

```bash
pip install -r requirements.txt
```

However, this may affect other Python projects on your system.

---

## 3. Pandoc (Required)

Used to convert Word documents (`.docx`) into Markdown.

Install:
https://pandoc.org/installing.html

### Check installation

```bash
pandoc --version
```

---

## 4. Quarto CLI (Required)

Used to render the final course website.

Install:
https://quarto.org/docs/get-started/

### Check installation

```bash
quarto --version
```

---

## 5. Running Commands (Important)

This project uses a `src/` layout. When running commands directly from the repository, you must set `PYTHONPATH`.

---

### macOS / Linux

```bash
PYTHONPATH=src python3 -m course_generator.cli build config/course.yml
```

---

### Windows (Command Prompt)

```cmd
set PYTHONPATH=src && python -m course_generator.cli build config/course.yml
```

---

### Windows (PowerShell)

```powershell
$env:PYTHONPATH="src"
python -m course_generator.cli build config/course.yml
```

---

## 6. System Check (Recommended)

Run these commands to confirm everything is working:

```bash
python --version
pandoc --version
quarto --version
```

---

## ✅ Summary

The system depends on:

- Python (execution environment)
- Pandoc (Word → Markdown conversion)
- Quarto (final rendering)

Recommended setup:

- Use a virtual environment (`.venv`) for isolation and safety
- Run commands from the project root directory

Additional note:

- `PYTHONPATH=src` is required when running commands without installing the package

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
