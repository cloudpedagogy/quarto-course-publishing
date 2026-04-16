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

### Install project dependencies

From the repository root:

```bash
pip install -r requirements.txt
```

> Note: `pip install -e .` is optional and only required if you want simplified CLI commands.

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

Additional note:

- `PYTHONPATH=src` is required when running commands without installing the package.
