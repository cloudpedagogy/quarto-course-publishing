# Quarto Course Generator

A schema-driven publishing system for generating flexible, pedagogically structured course websites and materials from configuration files.

> [!IMPORTANT]
> **Authoritative Guide**: Please refer to [USER_GUIDE.md](USER_GUIDE.md) for detailed instructions on the Architect/Publish/Preview workflow.

## Features

- **Hierarchical Structure**: Organise courses through the **Module → Session → Section → Page** model.
- **Smart Interaction Sync**: Safely edit pedagogical blocks (quizzes, accordions, etc.). Your content is preserved during structural rebuilds.
- **Pedagogical Interaction Kit**: 22+ built-in interactions including `self_check`, `quiz_check`, `code_along`, and `math_explanation`.
- **Variant System**: Control styles (e.g., `warning` vs `tip`) via simple YAML flags.
- **Stable 3-Step Workflow**: Standardized `build`, `render`, and `preview` CLI commands.

## Installation

```bash
pip install -r requirements.txt
pip install -e .
```

## Project Structure

- `config/`: Course architecture blueprints (e.g., `epm102.yml`).
- `course/{module_id}/`: **Source Workspace**. Edit your `.qmd` files here.
- `output/{module_id}/`: Final rendered website.
- `templates/`: Jinja2 templates for pages and interactions.
- `src/`: Core Python logic (Generator, CLI, Resolver).

## Quick Start (CLI)

### 1. Build a Course (Architect)
```bash
PYTHONPATH=src python3 -m course_generator.cli build config/course.yml
```

### 2. Preview a Page (Iterative)
```bash
PYTHONPATH=src python3 -m course_generator.cli preview config/course.yml --path path/to/page.qmd
```

### 3. Render Site (Publish)
```bash
PYTHONPATH=src python3 -m course_generator.cli render config/course.yml
```

## Developer Info

- **Source Code**: `src/course_generator`
- **Templates**: `templates/`
- **Tests**: `tests/`
- **User Guide**: `USER_GUIDE.md`

## Word Content Import (Prototype)

The system now supports importing content from Word documents (`.docx`) into generated Quarto pages.

### Usage
```bash
PYTHONPATH=src python3 -m course_generator.cli import-word config/course.yml
```

### Features
- **Idempotent**: Uses `<!-- IMPORT_START -->` markers to identify and replace imported content without duplication.
- **Safe**: Automatically creates a `.bak` backup of any modified `.qmd` file.
- **Conversion**: Uses Pandoc to convert Word content to GitHub Flavored Markdown (GFM).
- **R Code Support**: Automatically detects `{r}` code blocks in Word and preserves them as fenced blocks in Quarto.
