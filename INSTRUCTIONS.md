# Operational Instructions: Quarto Course Publishing

This guide provides step-by-step instructions for setting up, authoring, and publishing courses using the publishing system.

## 1. Environment Setup

### 1.1. Prerequisites
- **Python 3.10+**
- **Quarto CLI** (v1.3+)
- **Pandoc** (for Word import feature)

### 1.2. Installation
```bash
# Clone the repository
git clone <remote-url>
cd lshtm-quarto-publishing

# Install dependencies
pip install -r requirements.txt

# Install the package in editable mode
pip install -e .
```

---

## 2. The CLI Workflow

The system provides three main commands via the `course_generator.cli` module.

### BUILD (Structural Phase)
Run this when you change `config/course.yml` (e.g., adding pages, reordering).
```bash
PYTHONPATH=src python3 -m course_generator.cli build config/course.yml
```
- **Syncing**: This command matches YAML IDs to existing files and updates metadata/navigation while preserving your written content.

### PREVIEW (Writing Phase)
Run this for rapid feedback on a single page.
```bash
PYTHONPATH=src python3 -m course_generator.cli preview config/course.yml --path course/mod/se/page.qmd
```
- Output is generated in a local `.preview/` folder.

### RENDER (Publishing Phase)
Run this to generate the entire website.
```bash
PYTHONPATH=src python3 -m course_generator.cli render config/course.yml
```
- Output is placed in `output/{module_id}/`.

---

## 3. Authoring Guide

### 3.1. Writing in Interaction Zones
The system allows you to write anywhere in the `.qmd` file. However, for structured blocks (like Quizzes), you must write inside the "Interaction Zones":

```markdown
<!-- editable:start content -->
*   Question: What is 2+2?
*   Answer: 4
<!-- editable:end -->
```

### 3.2. Page Kinds
When defining a page in `course.yml`, set the `kind` field to use a specific scaffold:
- `concept_page`: Theory and definitions.
- `worked_example`: Step-by-step models.
- `methods_page`: Protocols and labs.
- `activity_page`: Student tasks.

### 3.3. Interaction Variants
Change the style of a block by updating the `variant` in YAML:
- `callout_emphasis`: `note`, `tip`, `warning`, `important`.
- `quiz_check`: `mcq`, `true_false`.

---

## 4. Word Content Import (Experimental)
To import content from a Word document into an existing course structure:
1. Ensure your `.qmd` file has `<!-- IMPORT_START -->` markers.
2. Run the import command:
```bash
PYTHONPATH=src python3 -m course_generator.cli import-word config/course.yml --docx path/to/content.docx --target course/path/to/page.qmd
```

---

## 5. Troubleshooting
- **YAML Validation Failed**: Ensure IDs are unique and no required fields (title, kind) are missing.
- **Content Lost**: Check the `_archive/` folder in the project root. The system moves orphaned content there instead of deleting it.
- **Broken Sidebar**: Run a full `render` command to refresh the Quarto navigation.
