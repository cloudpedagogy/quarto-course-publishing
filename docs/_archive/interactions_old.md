# Quarto Course Interaction Reference

This reference documents the available interaction types and variants for the Quarto course generator. Authors can add these interactions to any `module`, `session`, `section`, or `page` in the course YAML.

## Usage Example

```yaml
interactions:
  - type: tabs
    variant: explanation_example
  - type: quiz
    variant: quick_check
    question_count: 3
```

---

## 1. Tabs
**Description:** Tabbed content scaffold.

### Variants:

#### `explanation_example`
- **Description:** Two tabs for Explanation and Example.
- **Default Tabs:**
  - Explanation
  - Example

#### `theory_practice_reflection`
- **Description:** Three tabs for Theory, Practice, and Reflection.
- **Default Tabs:**
  - Theory
  - Practice
  - Reflection

---

## 2. Reveal
**Description:** Collapsible content block (e.g., for solutions).

### Variants:

#### `worked_solution`
- **Description:** A collapsible block with the title "Worked Solution".
- **Default Title:** "Worked Solution"

---

## 3. Quiz
**Description:** Quiz scaffold with multiple choice placeholders.

### Variants:

#### `quick_check`
- **Description:** A quick quiz section.
- **Default Question Count:** 3

---

## Customizing Interactions

You can override default parameters in the YAML:

```yaml
interactions:
  - type: tabs
    tabs:
      - label: Custom Tab 1
      - label: Custom Tab 2
  - type: quiz
    question_count: 5
```
