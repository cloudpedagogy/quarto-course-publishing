# Course Author’s Guide: Mastering the Generation Workflow

Welcome! This guide explains how to use the **Pedagogical Course Generator** to build structured, professional Quarto course websites. This system follows a **"Scaffold-First"** philosophy: you define the architecture in YAML, and the system builds the "bones" while you write the "flesh."

---

## 🏗️ 1. Overview: The Scaffold-First Philosophy

*   **The Blueprint (`config/course.yml`)**: This is where you define the structure (Modules, Sessions, Pages).
*   **The Source (`course/{module_id}/`)**: This is where you write your teaching content in `.qmd` files.
*   **The Output (`output/{module_id}/`)**: This is the final website that students see.

---

## 🚀 2. The Workflow (3 Simple Steps)

The system uses three primary commands executed via the CLI:

### Step 1: BUILD (Architect Phase)
Use this command whenever you change the **structure** of your course (add pages, reorder sections, or change interaction types).
```bash
PYTHONPATH=src python3 -m course_generator.cli build config/course.yml
```
*   **Behaviour**: It detects changes in your YAML and updates the `.qmd` files. It is **Non-Destructive** (your writing is safe!). **Versioning is active by default**—if the folder exists, the system automatically creates a new version (e.g., `_v1`).

### Step 2: PREVIEW (Iterative Writing)
Use this while writing content on a single page to get instant feedback.
```bash
PYTHONPATH=src python3 -m course_generator.cli preview config/course.yml --path course/mod001/se01/page.qmd
```
*   **Simple Rule**: This renders **one single page** for rapid testing. It does **not** affect your published website or update any navigation links. The results appear in a local `.preview/` folder.

### Step 3: RENDER (Publishing Phase)
Use this when you are ready to publish the full course website.
```bash
PYTHONPATH=src python3 -m course_generator.cli render config/course.yml
```
*   **Behaviour**: It renders every page, generates navigation, and places the final site in `output/{id}/`. **Versioning is active by default** to ensure you always have a backup of your previous site.

---

## 📂 3. Folder Structure

*   `config/`: Store your course YAML blueprints here.
*   `course/{module_id}/`: **This is your workspace.** Edit the `.qmd` files here.
*   `output/{module_id}/`: The finished website. **Do not edit files here.**
*   `templates/`: The pedagogical "DNA" of your course (Pages and Interactions).

---

## ✍️ 4. Editing Content (.qmd)

When you open a page in `course/`, you will see two types of areas:

### The Page Body
This is the main area where you write your lesson. Anything outside special markers is **yours** and will never be touched by the system.

### Interaction Zones
These are pedagogical blocks (like Quizzes or Accordions) wrapped in system markers. 
*   **Safety Rule**: Only edit text inside `<!-- editable:start -->` and `<!-- editable:end -->` tags.
*   **Example**:
    ```markdown
    <!-- editable:start content -->
    YOUR TEACHING CONTENT GOES HERE.
    <!-- editable:end -->
    ```

---

## 🛠️ 5. Editing Structure (course.yml)

The `course.yml` file uses a simple hierarchy:
1.  **Module**: Global code and title.
2.  **Session**: High-level groups (e.g., Week 1).
3.  **Section**: Pedagogical units (e.g., Introduction).
4.  **Page**: Individual learning pages.

### Page Types: When to Use Them
Choose from 15+ specialized scaffolds based on your pedagogical goal:
*   `overview_page`: **Section Introductions**. Use this to frame the module and explain "Why this matters."
*   `concept_page`: **Core Theory**. The primary space for teaching concepts and definitions.
*   `worked_example`: **Demonstrations**. Show a model solution or expert walkthrough.
*   `activity_page`: **Active Practice**. Scaffolds for student tasks and instructions.
*   `methods_page`: **Technical Processes**. Use for "How-to" guides, lab protocols, or coding steps.

---

🧩 6. Interactions & Variants

Interactions are **ordered pedagogical blocks** that appear exactly in the sequence you define in the YAML.

```yaml
interactions:
  - type: callout_emphasis
    variant: warning
    label: "Critical Tip"
  - type: self_check
    variant: deep
```

### Core Interaction Types
*   `callout_emphasis`: **Highlight Keys.** Use for tips, warnings, or "Stop & Think" moments.
*   `self_check`: **Quick Recall.** Low-stakes questions to help learners check their understanding.
*   `quiz_check`: **Knowledge Checks.** Formative assessment with feedback/rationale.
*   `compare_tabs`: **Multiple Perspectives.** Compare two different approaches or theories side-by-side.
*   `reveal_sequence`: **Step-by-Step Insight.** Hide answers or complex explanations until the learner is ready.
*   `scenario_response`: **Applied Logic.** Challenge learners to apply theory to a real-world situation.

### Supported Variants (v1)
Variants allow you to change the **style** or **format** of a block without changing its content.
*   `callout_emphasis`: `note`, `tip`, `warning`, `important`.
*   `quiz_check`: `mcq`, `true_false`, `short_answer`.
*   `reflection_prompt`: `guided`, `open`, `critical`.

---

## 🔄 7. Smart Interaction Sync (Non-Destructive)

The system is built for **Real Academic Authoring**. It understands the difference between the "bones" of the course (system-managed) and the "flesh" (your teaching content).

### How it Works (Under the Hood)
When you run the `build` command, the system performs a surgical three-step update:
1.  **Extract**: It scans your existing `.qmd` files and safely extracts any text you've written inside "Interaction Zones."
2.  **Rebuild**: It discards the old template container and builds a fresh one based on the latest YAML (applying new styles or variants).
3.  **Reinsert**: It perfectly re-injects your extracted writing back into the brand-new containers.

### Reassurance for Real-World Changes
*   **Reordering**: If you move an interaction up or down in the YAML, your text simply "moves" with it to the new position.
*   **Changing Variants**: If you change a `callout_emphasis` from a `note` to a `warning`, the system updates the visual box style but **perfectly preserves your writing** inside.
*   **Adding/Removing**: New interactions are added as stubs; removed interactions are safely backed up in the `_archive/` folder. **We never delete your work.**

> [!IMPORTANT]
> **Safety First**: Your content is safe *as long as you do not delete* the `<!-- editable:start -->` markers. These tags are the maps the system uses to find and protect your writing.

---

## 🛠️ 8. Common Tasks

### Adding a New Page
1.  Open your `course.yml` blueprint.
2.  Add a new entry under the `subpages:` list in the desired section.
3.  Run the **Build** command.
4.  **Result**: A new `.qmd` file appears in your course folder, pre-formatted and ready for writing.

### Moving or Reordering Pages
1.  Rearrange the pages in your `course.yml` file.
2.  Run the **Build** command.
3.  **Result**: The system automatically renames the files to match the new order and updates their internal identity tags.

### Deleting a Page
1.  Remove the page entry from your `course.yml`.
2.  Run the **Build** command.
3.  **Result**: The file is removed from your active workspace and safely moved to an `_archive/` folder.

### Adding an Interaction
1.  In `course.yml`, add a new `type:` under the page's `interactions:` list.
2.  Run the **Build** command.
3.  **Result**: A new pedagogical block appears on your page with `[AUTHOR GUIDE:]` markers explaining how to fill it in.

---

## ⚠️ 9. Safety & Best Practices

1.  **Do Not Delete Markers**: Never delete `<!-- START_INTERACTIONS -->` or `<!-- editable:... -->` tags. These are the safety guards that allow the system to protect your content.
2.  **YAML for Structure**: Any changes to page order, titles, or site structure **must** be done in the `course.yml` first.
3.  **Do Not Move Files Manually**: Moving or renaming `.qmd` files using your computer's file explorer will break the link with the blueprint. Always let the `build` command handle file relocation.

---

## 🩺 10. Troubleshooting

*   **YAML Error**: "expected <block end>." Check your indentation. YAML is very sensitive to spaces—always use exactly two spaces per level.
*   **Missing Content**: Ensure you haven't deleted the `<!-- editable -->` markers. If content is missing after a build, check the `_archive/` folder.
*   **Broken Links**: Run a full **Render** to refresh the site navigation and cross-links.

---
**Happy Authoring!** Your content is safe, and your structure is stable.
