import os
import shutil
import subprocess
from pathlib import Path
import click
import re
from ..core.config_loader import ConfigLoader

IMPORT_START = "<!-- IMPORT_START -->"
IMPORT_END = "<!-- IMPORT_END -->"

def check_pandoc():
    """Check if pandoc is installed and available in PATH."""
    return shutil.which("pandoc") is not None

def convert_docx_to_md(docx_path: Path, md_path: Path):
    """Convert a DOCX file to Markdown using Pandoc."""
    # Use standard markdown for the primary conversion with no wrapping to aid parsing
    cmd = ["pandoc", str(docx_path), "-t", "markdown", "--wrap=none", "-o", str(md_path)]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"Pandoc conversion failed: {result.stderr}")

def parse_r_code(content: str) -> tuple[str, int]:
    """Detects 'R Code' sections and wraps subsequent lines into standard Quarto fenced code blocks."""
    import re
    lines = content.split('\n')
    new_lines = []
    count = 0
    in_code_block = False
    
    for line in lines:
        stripped = line.strip()
        
        if not in_code_block:
            # Detect an explicitly mapped R Code section (e.g. ## R Code or R Code)
            if re.match(r'^(?:#+\s*)?R Code\s*$', stripped, re.IGNORECASE):
                new_lines.append(line)       # Preserve the heading
                new_lines.append("```{r}")   # Open the code fence
                in_code_block = True
                count += 1
            else:
                new_lines.append(line)
        else:
            # We are inside an R code block
            # Stop accumulating code upon reaching the next logical section heading
            if re.match(r'^#+\s+', stripped):
                new_lines.append("```")      # Close the code fence
                new_lines.append("")
                new_lines.append(line)       # Emit the heading that triggered the close
                in_code_block = False
            else:
                # Strip out manually authored $\{r\}$ or `{r}` if present, as it's handled by fence opening
                if stripped not in ["{r}", "`{r}`"]:
                    new_lines.append(line)
                
    if in_code_block:
        new_lines.append("```")
        
    if count > 0:
        click.echo(click.style(f"Detected R code blocks", fg='blue'))
        click.echo(f"  Rendering {count} fenced code chunks")
        
    return "\n".join(new_lines), count

def parse_tabs(content: str) -> tuple[str, int]:
    """Detects and renders localized Tab interactions (Quarto tabset)."""
    import re
    lines = content.split('\n')
    new_lines = []
    count = 0
    
    in_tabs = False
    current_tab_title = None
    tab_content_lines = []
    
    def flush_tab():
        if current_tab_title:
            new_lines.append(f"## {current_tab_title}")
            new_lines.append("\n".join(tab_content_lines).strip())
            new_lines.append("")
    
    for line in lines:
        stripped = line.strip()
        
        if not in_tabs:
            if re.match(r'^(?:#+\s*)?Tabs$', stripped):
                in_tabs = True
                new_lines.append("::: {.panel-tabset}")
                count += 1
                current_tab_title = None
                tab_content_lines = []
                continue
            else:
                new_lines.append(line)
        else:
            # Inside tabs module. Check if it is a new markdown heading breaking the flow
            if re.match(r'^#+\s+', stripped):
                flush_tab()
                new_lines.append(":::")
                new_lines.append(line)
                in_tabs = False
                current_tab_title = None
                tab_content_lines = []
            elif "::" in stripped:
                # New tab definition
                flush_tab()
                current_tab_title, tab_content = stripped.split("::", 1)
                current_tab_title = current_tab_title.strip()
                tab_content_lines = [tab_content.strip()]
            else:
                # Continuation of content in current tab
                if current_tab_title is not None:
                    tab_content_lines.append(line)
                else:
                    if stripped:
                        tab_content_lines.append(line)
    
    if in_tabs:
        flush_tab()
        new_lines.append(":::")

    if count > 0:
        click.echo(click.style(f"Detected tabs interaction", fg='blue'))
        click.echo(f"  Rendering as tabset")
    
    return "\n".join(new_lines), count

def parse_interactions(content: str) -> str:
    """Coordinator function for parsing all interaction types."""
    total_interactions = 0
    
    content, count = parse_tabs(content)
    total_interactions += count
    
    content, count = parse_r_code(content)
    total_interactions += count
    
    # Future parsers can be added here easily.
    # content, count = parse_reveal(content)
    # total_interactions += count
    
    if total_interactions == 0:
        click.echo(f"  No interaction patterns detected")
        
    return content

def insert_markdown_into_qmd(md_path: Path, qmd_path: Path):
    """
    Inserts Markdown content into a QMD file.
    - Creates a .bak backup.
    - Uses IMPORT_START/END markers for idempotency.
    - If markers are missing, inserts after the frontmatter's second ---.
    """
    if not qmd_path.exists():
        raise FileNotFoundError(f"Target QMD file not found: {qmd_path}")

    # Read imported content
    with open(md_path, 'r') as f:
        imported_content = f.read()

    # Process interactions (e.g., Tabs) before insertion
    imported_content = parse_interactions(imported_content).strip()

    # Strip the top-level H1 or Title heading to prevent duplication with the QMD YAML title.
    # This specifically removes the first line if it's `# Something` or `Title: Something`.
    imported_content = re.sub(r'^\s*#\s+[^\n]*\n*', '', imported_content, count=1)
    imported_content = re.sub(r'^\s*Title:\s*[^\n]*\n*', '', imported_content, count=1, flags=re.IGNORECASE)
    imported_content = imported_content.strip()

    # Read target QMD
    with open(qmd_path, 'r') as f:
        qmd_content = f.read()

    # 1. Create Backup
    backup_path = qmd_path.with_suffix(qmd_path.suffix + ".bak")
    shutil.copy2(qmd_path, backup_path)

    # 2. Prepare Insertion (Markers)
    new_imported_block = f"\n\n{IMPORT_START}\n\n{imported_content}\n\n{IMPORT_END}\n"

    if IMPORT_START in qmd_content and IMPORT_END in qmd_content:
        # Replacement (Idempotent)
        pattern = re.escape(IMPORT_START) + r".*?" + re.escape(IMPORT_END)
        # We use a replacement that includes the markers back in
        new_qmd_content = re.sub(pattern, f"{IMPORT_START}\n\n{imported_content}\n\n{IMPORT_END}", qmd_content, flags=re.DOTALL)
    else:
        # Initial Insertion after frontmatter
        fm_pattern = r'^---\s*\n.*?\n---\s*\n'
        fm_match = re.search(fm_pattern, qmd_content, re.DOTALL)
        
        if fm_match:
            insert_pos = fm_match.end()
            new_qmd_content = qmd_content[:insert_pos] + new_imported_block + qmd_content[insert_pos:]
        else:
            # Fallback if no frontmatter? Prepend.
            new_qmd_content = new_imported_block + qmd_content

    # 3. Write back
    with open(qmd_path, 'w') as f:
        f.write(new_qmd_content)

def run_import(config_path: str):
    """Orchestrates the import workflow."""
    if not check_pandoc():
        click.echo(click.style("Pandoc is not installed. Please install Pandoc to use import-word.", fg='red'), err=True)
        return

    try:
        config = ConfigLoader.load(config_path)
        course_id = config.module.id.lower()
        click.echo(f"Importing Word content for course: {course_id}")

        # Setup paths
        import_dir = Path("imports") / course_id
        docx_dir = import_dir / "docx"
        md_dir = import_dir / "md"
        md_dir.mkdir(parents=True, exist_ok=True)
        
        course_dir = Path("course") / course_id
        # Collision: Find the correct directory if versioning was used
        if not course_dir.exists():
            parent = course_dir.parent
            options = [d for d in parent.iterdir() if d.is_dir() and d.name.startswith(course_id)]
            if not options:
                click.echo(click.style(f"Error: Course directory {course_dir} not found. Run 'build' first.", fg='red'), err=True)
                return
            course_dir = sorted(options)[-1]

        click.echo(f"Locating target files in: {course_dir}")

        # Hardcoded Mapping for Demo
        mapping = {
            "01_binomial_concept.docx": "BINOMIAL_DISTRIBUTION-se01-sec01-sp01.qmd",
            "02_binomial_worked_example.docx": "BINOMIAL_DISTRIBUTION-se01-sec01-sp02.qmd",
            "03_binomial_activity.docx": "BINOMIAL_DISTRIBUTION-se01-sec01-sp03.qmd"
        }

        for docx_name, target_qmd_name in mapping.items():
            docx_path = docx_dir / docx_name
            if not docx_path.exists():
                click.echo(click.style(f"Warning: {docx_name} not found in {docx_dir}. Skipping.", fg='yellow'))
                continue

            md_path = md_dir / docx_path.with_suffix(".md").name
            click.echo(f"Converting {docx_name} to Markdown")
            convert_docx_to_md(docx_path, md_path)
            click.echo(f"  Saved to {md_path}")

            # Find target QMD file
            target_path = None
            for root, _, files in os.walk(course_dir):
                if target_qmd_name in files:
                    target_path = Path(root) / target_qmd_name
                    break
            
            if target_path:
                click.echo(f"Locating target page {target_qmd_name}")
                click.echo(f"Inserting converted content into {target_path}")
                insert_markdown_into_qmd(md_path, target_path)
            else:
                click.echo(click.style(f"Error: Target {target_qmd_name} not found in {course_dir}.", fg='red'))

        click.echo(click.style("✅ Import complete.", fg='green'))

    except Exception as e:
        click.echo(click.style(f"Error: {str(e)}", fg='red'), err=True)
