# PREREQUISITES.md

## ⚙️ System Prerequisites

Before using the Quarto Course Publishing System, ensure the following are installed.

---

## 1. Python Environment

- Python **3.10 or higher**

### Check version

**macOS / Linux**
```bash
python3 --version
```

**Windows**
```cmd
python --version
```

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

## 2. Pandoc (Required)

Used to convert Word documents (`.docx`) into Markdown.

Install:
https://pandoc.org/installing.html

### Check installation

```bash
pandoc --version
```

---

## 3. Quarto CLI (Required)

Used to render the final course website.

Install:
https://quarto.org/docs/get-started/

### Check installation

```bash
quarto --version
```

---

## 4. Running Commands (Important)

This project uses a `src/` layout. When running commands directly from the repository, you must set `PYTHONPATH`.

---

### macOS / Linux

```bash
PYTHONPATH=src python3 -m course_generator.cli build config/course.yml
```

---

### Windows (Command Prompt)

```cmd
set PYTHONPATH=src
python -m course_generator.cli build config/course.yml
```

---

### Windows (PowerShell)

```powershell
$env:PYTHONPATH="src"
python -m course_generator.cli build config/course.yml
```

---

## 5. System Check (Recommended)

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
