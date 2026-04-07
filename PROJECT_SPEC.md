# Project Specification: Quarto Course Publishing System

## 1. Executive Summary
The Quarto Course Publishing System is a schema-driven content engine designed to build structured, professional Quarto course websites. Its core philosophy is "Scaffold-First," where course architecture is defined in YAML, and the system manages the "bones" (structure and pedagogy) while authors write the "flesh" (content).

## 2. Technical Stack
- **Languages**: Python 3.10+
- **Markup**: Quarto (.qmd), Markdown (GFM)
- **Templating**: Jinja2
- **Data Validation**: Pydantic
- **CLI Framework**: Python `argparse`
- **Infrastructure**: Git (for version control and collaboration)

## 3. Core Architecture

### 3.1. Hierarchy Models
The system follows a strict pedagogical hierarchy:
1.  **Module**: The top-level wrapper (e.g., PH101).
2.  **Session**: High-level grouping (e.g., Week 1, Introduction).
3.  **Section**: A unit of learning within a session.
4.  **Page**: The individual learning object (The atomic unit).

### 3.2. Components
- **`Generator`**: Orchestrates the build process, manages cross-links, navigation, and file sync.
- **`InteractionResolver`**: Dynamically renders pedagogical blocks (quizzes, callouts) based on YAML definitions.
- **`PageKindResolver`**: Applies layout scaffolds based on the `kind` of page (e.g., `concept_page`, `worked_example`).
- **`TemplateManager`**: Handles Jinja2 environment and partial rendering.

## 4. Key Features

### 4.1. Non-Destructive Sync (Idempotency)
The system uses **Engagement Markers** to identify managed zones in the `.qmd` files. This allows the system to update the structure, styles, and navigation without overwriting author content written in designated "Interaction Zones."

### 4.2. Smart Content Extraction
When a course is "rebuilt," the system surgically extracts content from `<!-- editable:start -->` blocks, rebuilds the template containers with new variants or order, and re-injects the content perfectly.

### 4.3. Pedagogical Interaction Kit
A library of 22+ built-in interactions that can be dropped into any page via YAML:
- **Assessment**: `quiz_check`, `self_check`.
- **Engagement**: `reveal_sequence`, `scenario_response`, `compare_tabs`.
- **Information Design**: `callout_emphasis`, `resource_block`.

### 4.4. Automatic Versioning
To prevent data loss and ensure stable releases, the system automatically versions output folders (e.g., `course/mod001_v1`, `course/mod001_v2`) when structural changes are detected.

## 5. Data Schema (YAML)
The `course.yml` configuration is validated against Pydantic models in `src/models/schema.py`. Key fields include:
- `id`: Unique identifier for the object (used for file naming and syncing).
- `kind`: The template type for pages.
- `interactions`: List of pedagogical blocks to render.
- `render_mode`: `single_page` vs `multi_page` output configurations.

## 6. Project Structure
```text
.
├── config/           # Course YAML blueprints
├── course/           # Source authoring workspace (tracked)
├── output/           # Rendered Quarto websites (ignored)
├── src/              # Core logic (Generator, CLI, Models)
├── templates/        # Jinja2 templates (Pages, Interactions, Nav)
├── tests/            # Automated test suite
└── PROJECT_SPEC.md   # [This Document]
```
