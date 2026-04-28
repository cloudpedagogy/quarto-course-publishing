import os
import shutil
import subprocess
from pathlib import Path
import click
import re
from urllib.parse import urlparse, parse_qs
from ..core.config_loader import ConfigLoader

IMPORT_START = "<!-- IMPORT_START -->"
IMPORT_END = "<!-- IMPORT_END -->"


def check_pandoc():
    """Check if pandoc is installed and available in PATH."""
    return shutil.which("pandoc") is not None


def convert_docx_to_md(docx_path: Path, md_path: Path):
    """Convert a DOCX file to Markdown using Pandoc."""
    cmd = ["pandoc", str(docx_path), "-t", "markdown", "--wrap=none", "-o", str(md_path)]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"Pandoc conversion failed: {result.stderr}")


def normalize_metadata_blocks(content: str) -> str:
    """
    Pandoc often converts directive-style Word content into markdown lines
    ending with backslashes. This function normalizes supported interaction
    blocks so downstream parsers can detect them reliably.
    """
    directive_starters = [
        "Callout ::",
        "Reveal",
        "SelfCheck",
        "R Code",
        "END R Code",
        "R Example",
        "END R Example",
        "Tabs",
        "Image ::",
        "File ::",
        "Quiz",
        "YouTubeEmbed ::",
        "PanoptoEmbed ::",
    ]

    directive_fields = [
        "Text ::",
        "Question ::",
        "Answer ::",
        "Option ::",
        "Explanation ::",
        "Interpretation ::",
        "Assumptions ::",
        "Limitations ::",
        "Alt ::",
        "Width ::",
        "Display ::",
        "Label ::",
        "Caption ::",
    ]

    lines = content.split("\n")
    normalized = []

    for line in lines:
        stripped = line.strip()

        if stripped.endswith("\\"):
            stripped = stripped[:-1].rstrip()

        if not stripped:
            normalized.append("")
            continue

        if re.match(r"^Step\s+\d+\s*::", stripped):
            normalized.append(stripped)
            continue

        if any(stripped.startswith(prefix) for prefix in directive_starters + directive_fields):
            normalized.append(stripped)
        else:
            normalized.append(line.rstrip())

    return "\n".join(normalized)


def normalize_math_blocks(content: str) -> str:
    """
    Unescape display-math delimiters that Pandoc may emit as literal text.
    """
    normalized_lines = []

    for line in content.split("\n"):
        stripped = line.strip()

        if stripped == r"\$\$":
            normalized_lines.append("$$")
        else:
            normalized_lines.append(line)

    return "\n".join(normalized_lines)


def clean_r_code(code: str) -> str:
    """
    Clean R code after Pandoc conversion.

    Fixes:
    - trailing backslashes
    - escaped symbols
    - removes artificial blank lines from Word/Pandoc
    """
    cleaned_lines = []

    for raw_line in code.splitlines():
        line = raw_line.rstrip()

        if line.endswith("\\"):
            line = line[:-1].rstrip()

        line = line.replace(r"\<-", "<-")
        line = line.replace(r"\"", '"')
        line = line.replace(r"\<", "<")
        line = line.replace(r"\>", ">")

        if line.strip():  # 🔥 removes blank lines
            cleaned_lines.append(line)

    return "\n".join(cleaned_lines).strip()


def rewrite_asset_path(asset_path: str, qmd_path: Path, course_dir: Path) -> str:
    """
    Rewrite a site-level asset path like 'resources/pdf/file.pdf' so it works
    from the nested location of the generated QMD/HTML page.
    """
    asset_path = asset_path.strip().replace("\\", "/")

    if not asset_path.startswith("resources/"):
        return asset_path

    qmd_parent = qmd_path.parent
    target_asset = course_dir / asset_path
    relative_path = os.path.relpath(target_asset, start=qmd_parent)
    return relative_path.replace("\\", "/")


def copy_site_resources(course_dir: Path):
    """
    Copy top-level project resources into the generated course directory so
    rendered HTML pages can link to them.
    """
    source_resources = Path("resources")
    if not source_resources.exists():
        click.echo(click.style("No top-level resources/ directory found; skipping resource copy", fg="yellow"))
        return

    dest_resources = course_dir / "resources"

    if dest_resources.exists():
        shutil.rmtree(dest_resources)

    shutil.copytree(source_resources, dest_resources)
    click.echo(f"Copied site resources to: {dest_resources}")


def is_markdown_heading(line: str) -> bool:
    return re.match(r"^#+\s+", line.strip()) is not None


def is_interaction_header(line: str) -> bool:
    stripped = line.strip()
    return any(
        re.match(pattern, stripped, re.IGNORECASE)
        for pattern in [
            r"^(?:#+\s*)?R Code\s*$",
            r"^(?:#+\s*)?END R Code\s*$",
            r"^(?:#+\s*)?R Example\s*$",
            r"^(?:#+\s*)?END R Example\s*$",
            r"^(?:#+\s*)?Tabs\s*$",
            r"^(?:#+\s*)?Reveal\s*$",
            r"^(?:#+\s*)?Quiz\s*$",
            r"^(?:#+\s*)?SelfCheck\s*$",
            r"^(?:#+\s*)?Callout\s*::",
            r"^(?:#+\s*)?Image\s*::",
            r"^(?:#+\s*)?File\s*::",
            r"^(?:#+\s*)?YouTubeEmbed\s*::",
            r"^(?:#+\s*)?PanoptoEmbed\s*::",
        ]
    )


def extract_youtube_id(url: str) -> str | None:
    """Extract a YouTube video ID from common YouTube URL formats."""
    url = url.strip()

    if "youtu.be/" in url:
        return url.split("youtu.be/")[-1].split("?")[0]

    if "youtube.com" in url:
        parsed = urlparse(url)
        return parse_qs(parsed.query).get("v", [None])[0]

    return None


def extract_panopto_id(url: str) -> str | None:
    """Extract the Panopto video/session id from a Panopto Viewer URL."""
    match = re.search(r"[?&]id=([a-zA-Z0-9\-]+)", url)
    return match.group(1) if match else None


def render_youtube_iframe(url: str) -> str:
    """Render a standard YouTube embed iframe from a URL."""
    video_id = extract_youtube_id(url)
    if not video_id:
        return f"<!-- Invalid YouTube URL: {url} -->"

    return (
        f'<iframe width="560" height="315" '
        f'src="https://www.youtube.com/embed/{video_id}" '
        f'title="YouTube video player" frameborder="0" '
        f'allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" '
        f'referrerpolicy="strict-origin-when-cross-origin" '
        f'allowfullscreen></iframe>'
    )


def render_panopto_iframe(url: str) -> str:
    """Render a Panopto embed iframe from a Panopto Viewer URL."""
    video_id = extract_panopto_id(url)
    if not video_id:
        return f"<!-- Invalid Panopto URL: {url} -->"

    parsed = urlparse(url)
    embed_url = f"{parsed.scheme}://{parsed.netloc}/Panopto/Pages/Embed.aspx?id={video_id}"

    return (
        f'<iframe src="{embed_url}" title="Panopto video player" width="720" height="405" '
        f'frameborder="0" allowfullscreen></iframe>'
    )


def validate_import_content(content: str, page_id: str = "", project_root: Path | None = None) -> list[str]:
    """
    Lightweight validation for common authoring mistakes.
    Returns warnings only; does not block import.
    """
    warnings = []
    lines = content.split("\n")
    project_root = project_root or Path(".")

    quiz_open = False
    quiz_start_line = None
    quiz_has_question = False
    quiz_option_count = 0
    quiz_has_answer = False

    for idx, raw_line in enumerate(lines, start=1):
        line = raw_line.strip()

        if not line:
            continue

        malformed_match = re.match(
            r"^(YouTubeEmbed|PanoptoEmbed|Image|File|Callout|Question|Option|Answer|Caption|Alt|Width|Display|Label)\s*:\s+\S+",
            line,
            re.IGNORECASE,
        )
        if malformed_match:
            warnings.append(f"{page_id} line {idx}: possible directive syntax error. Use '::' not ':'.")

        if re.match(r"^(?:#+\s*)?Quiz\s*$", line, re.IGNORECASE):
            if quiz_open:
                if not quiz_has_question:
                    warnings.append(f"{page_id} line {idx}: previous Quiz block missing Question ::")
                if quiz_option_count < 2:
                    warnings.append(f"{page_id} line {idx}: previous Quiz block has fewer than 2 Option :: lines")
                if not quiz_has_answer:
                    warnings.append(f"{page_id} line {idx}: previous Quiz block missing Answer ::")

            quiz_open = True
            quiz_start_line = idx
            quiz_has_question = False
            quiz_option_count = 0
            quiz_has_answer = False
            continue

        if quiz_open and (is_markdown_heading(raw_line) or is_interaction_header(raw_line)):
            if not quiz_has_question:
                warnings.append(f"{page_id} line {quiz_start_line}: Quiz block missing Question ::")
            if quiz_option_count < 2:
                warnings.append(f"{page_id} line {quiz_start_line}: Quiz block has fewer than 2 Option :: lines")
            if not quiz_has_answer:
                warnings.append(f"{page_id} line {quiz_start_line}: Quiz block missing Answer ::")
            quiz_open = False
            quiz_start_line = None

        if quiz_open:
            if re.match(r"^Question\s*::\s*(.+)$", line, re.IGNORECASE):
                quiz_has_question = True
            elif re.match(r"^Option\s*::\s*(.+)$", line, re.IGNORECASE):
                quiz_option_count += 1
            elif re.match(r"^Answer\s*::\s*(.+)$", line, re.IGNORECASE):
                quiz_has_answer = True

        yt_match = re.match(r"^(?:#+\s*)?YouTubeEmbed\s*::\s*(.+)$", line, re.IGNORECASE)
        if yt_match:
            url = yt_match.group(1).strip()
            if not extract_youtube_id(url):
                warnings.append(f"{page_id} line {idx}: invalid YouTube URL")

        pan_match = re.match(r"^(?:#+\s*)?PanoptoEmbed\s*::\s*(.+)$", line, re.IGNORECASE)
        if pan_match:
            url = pan_match.group(1).strip()
            if not extract_panopto_id(url):
                warnings.append(f"{page_id} line {idx}: invalid Panopto URL")

        img_match = re.match(r"^(?:#+\s*)?Image\s*::\s*(.+)$", line, re.IGNORECASE)
        if img_match:
            raw_path = img_match.group(1).strip().replace("\\", "/")
            if raw_path.startswith("resources/") and not (project_root / raw_path).exists():
                warnings.append(f"{page_id} line {idx}: image path not found: {raw_path}")

        file_match = re.match(r"^(?:#+\s*)?File\s*::\s*(.+)$", line, re.IGNORECASE)
        if file_match:
            raw_path = file_match.group(1).strip().replace("\\", "/")
            if raw_path.startswith("resources/") and not (project_root / raw_path).exists():
                warnings.append(f"{page_id} line {idx}: file path not found: {raw_path}")

    if quiz_open:
        if not quiz_has_question:
            warnings.append(f"{page_id} line {quiz_start_line}: Quiz block missing Question ::")
        if quiz_option_count < 2:
            warnings.append(f"{page_id} line {quiz_start_line}: Quiz block has fewer than 2 Option :: lines")
        if not quiz_has_answer:
            warnings.append(f"{page_id} line {quiz_start_line}: Quiz block missing Answer ::")

    return warnings


def print_validation_warnings(warnings: list[str]):
    if warnings:
        click.echo(click.style("Validation warnings:", fg="yellow"))
        for warning in warnings:
            click.echo(click.style(f"  - {warning}", fg="yellow"))


def parse_r_example(content: str) -> tuple[str, int]:
    """
    Detect 'R Example' sections and render them as non-executing
    display-only R code blocks.

    Preferred syntax:

    R Example
    <R code>
    END R Example
    """
    lines = content.split("\n")
    new_lines = []
    count = 0

    in_code_block = False
    code_lines = []

    def flush_code_block():
        nonlocal code_lines, new_lines
        cleaned_code = clean_r_code("\n".join(code_lines))
        new_lines.append("```r")
        if cleaned_code:
            new_lines.append(cleaned_code)
        new_lines.append("```")
        code_lines = []

    for line in lines:
        stripped = line.strip()

        if not in_code_block:
            if re.match(r"^(?:#+\s*)?R Example\s*$", stripped, re.IGNORECASE):
                in_code_block = True
                count += 1
                code_lines = []
                continue
            else:
                new_lines.append(line)
        else:
            if re.match(r"^END\s+R\s+Example\s*$", stripped.strip(), re.IGNORECASE):
                flush_code_block()
                in_code_block = False
                continue

            if is_markdown_heading(line) or (
                is_interaction_header(line)
                and not re.match(r"^(?:#+\s*)?R Example\s*$", stripped, re.IGNORECASE)
            ):
                flush_code_block()
                new_lines.append("")
                new_lines.append(line)
                in_code_block = False
            else:
                if stripped not in ["{r}", "`{r}`", "```{r}", "```", "```r"]:
                    code_lines.append(line)

    if in_code_block:
        flush_code_block()

    if count > 0:
        click.echo(click.style("Detected R example blocks", fg="blue"))
        click.echo(f"  Rendering {count} non-executing R examples")

    return "\n".join(new_lines), count


def parse_r_code(content: str) -> tuple[str, int]:
    """
    Detect 'R Code' sections and wrap subsequent lines into executable
    Quarto fenced R code blocks.

    Preferred syntax:

    R Code
    Alt :: Description of generated figure
    Caption :: Visible figure caption
    <R code>
    END R Code
    """
    lines = content.split("\n")
    new_lines = []
    count = 0

    in_code_block = False
    code_lines = []
    fig_alt = ""
    fig_cap = ""

    def escape_chunk_option_text(text: str) -> str:
        return text.replace("\\", "\\\\").replace('"', '\\"')

    def flush_code_block():
        nonlocal code_lines, new_lines, fig_alt, fig_cap

        cleaned_code = clean_r_code("\n".join(code_lines))

        new_lines.append("```{r}")

        if fig_alt:
            new_lines.append(f'#| fig-alt: "{escape_chunk_option_text(fig_alt)}"')
        if fig_cap:
            new_lines.append(f'#| fig-cap: "{escape_chunk_option_text(fig_cap)}"')

        if cleaned_code:
            new_lines.append(cleaned_code)

        new_lines.append("```")

        code_lines = []
        fig_alt = ""
        fig_cap = ""

    for line in lines:
        stripped = line.strip()

        if not in_code_block:
            if re.match(r"^(?:#+\s*)?R Code\s*$", stripped, re.IGNORECASE):
                in_code_block = True
                count += 1
                code_lines = []
                fig_alt = ""
                fig_cap = ""
                continue
            else:
                new_lines.append(line)
        else:
            if re.match(r"^(?:#+\s*)?END R Code\s*$", stripped, re.IGNORECASE):
                flush_code_block()
                in_code_block = False
                continue

            if is_markdown_heading(line) or (
                is_interaction_header(line)
                and not re.match(r"^(?:#+\s*)?R Code\s*$", stripped, re.IGNORECASE)
            ):
                flush_code_block()
                new_lines.append("")
                new_lines.append(line)
                in_code_block = False
            else:
                alt_match = re.match(r"^Alt\s*::\s*(.*)$", stripped, re.IGNORECASE)
                cap_match = re.match(r"^Caption\s*::\s*(.*)$", stripped, re.IGNORECASE)

                if alt_match:
                    fig_alt = alt_match.group(1).strip()
                elif cap_match:
                    fig_cap = cap_match.group(1).strip()
                elif stripped not in ["{r}", "`{r}`", "```{r}", "```"]:
                    code_lines.append(line)

    if in_code_block:
        flush_code_block()

    if count > 0:
        click.echo(click.style("Detected R code blocks", fg="blue"))
        click.echo(f"  Rendering {count} fenced code chunks")

    return "\n".join(new_lines), count


def parse_tabs(content: str) -> tuple[str, int]:
    """Detect and render localized Tab interactions (Quarto tabset)."""
    lines = content.split("\n")
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
            if re.match(r"^(?:#+\s*)?Tabs\s*$", stripped, re.IGNORECASE):
                in_tabs = True
                new_lines.append("::: {.panel-tabset}")
                count += 1
                current_tab_title = None
                tab_content_lines = []
                continue
            else:
                new_lines.append(line)
        else:
            if is_markdown_heading(line) or (
                is_interaction_header(line)
                and not re.match(r"^(?:#+\s*)?Tabs\s*$", stripped, re.IGNORECASE)
            ):
                flush_tab()
                new_lines.append(":::")
                new_lines.append(line)
                in_tabs = False
                current_tab_title = None
                tab_content_lines = []
            elif "::" in stripped:
                flush_tab()
                current_tab_title, tab_content = stripped.split("::", 1)
                current_tab_title = current_tab_title.strip()
                tab_content_lines = [tab_content.strip()]
            else:
                if current_tab_title is not None:
                    tab_content_lines.append(line)
                elif stripped:
                    tab_content_lines.append(line)

    if in_tabs:
        flush_tab()
        new_lines.append(":::")

    if count > 0:
        click.echo(click.style("Detected tabs interaction", fg="blue"))
        click.echo("  Rendering as tabset")

    return "\n".join(new_lines), count


def parse_callouts(content: str) -> tuple[str, int]:
    lines = content.split("\n")
    new_lines = []
    count = 0
    i = 0

    while i < len(lines):
        stripped = lines[i].strip()
        match = re.match(r"^(?:#+\s*)?Callout\s*::\s*(.+)$", stripped, re.IGNORECASE)

        if not match:
            new_lines.append(lines[i])
            i += 1
            continue

        callout_type = match.group(1).strip().lower()
        text_lines = []
        i += 1

        while i < len(lines):
            s = lines[i].strip()
            if is_markdown_heading(lines[i]) or is_interaction_header(lines[i]):
                break

            field_match = re.match(r"^Text\s*::\s*(.*)$", s, re.IGNORECASE)
            if field_match:
                text_lines.append(field_match.group(1).strip())
            elif s:
                text_lines.append(lines[i].strip())

            i += 1

        new_lines.append(f"::: {{.callout-{callout_type}}}")
        if text_lines:
            new_lines.append("\n".join(text_lines).strip())
        new_lines.append(":::")
        new_lines.append("")
        count += 1

    if count > 0:
        click.echo(click.style("Detected callouts", fg="blue"))
        click.echo(f"  Rendering {count} callout blocks")

    return "\n".join(new_lines), count


def parse_selfcheck(content: str) -> tuple[str, int]:
    lines = content.split("\n")
    new_lines = []
    count = 0
    i = 0

    while i < len(lines):
        stripped = lines[i].strip()

        if not re.match(r"^(?:#+\s*)?SelfCheck\s*$", stripped, re.IGNORECASE):
            new_lines.append(lines[i])
            i += 1
            continue

        question = ""
        answer_lines = []
        i += 1

        while i < len(lines):
            s = lines[i].strip()
            if is_markdown_heading(lines[i]) or is_interaction_header(lines[i]):
                break

            q_match = re.match(r"^Question\s*::\s*(.*)$", s, re.IGNORECASE)
            a_match = re.match(r"^Answer\s*::\s*(.*)$", s, re.IGNORECASE)

            if q_match:
                question = q_match.group(1).strip()
            elif a_match:
                answer_lines.append(a_match.group(1).strip())
            elif s:
                answer_lines.append(lines[i].strip())

            i += 1

        new_lines.append("::: {.callout-tip}")
        if question:
            new_lines.append(f"**Self-check:** {question}")
            new_lines.append("")
        if answer_lines:
            new_lines.append("**Suggested answer**")
            new_lines.append("")
            new_lines.append("\n".join(answer_lines).strip())
        new_lines.append(":::")
        new_lines.append("")
        count += 1

    if count > 0:
        click.echo(click.style("Detected self-check blocks", fg="blue"))
        click.echo(f"  Rendering {count} self-check interactions")

    return "\n".join(new_lines), count


def parse_reveal(content: str) -> tuple[str, int]:
    lines = content.split("\n")
    new_lines = []
    count = 0
    i = 0

    while i < len(lines):
        stripped = lines[i].strip()

        if not re.match(r"^(?:#+\s*)?Reveal\s*$", stripped, re.IGNORECASE):
            new_lines.append(lines[i])
            i += 1
            continue

        step_lines = []
        i += 1

        while i < len(lines):
            s = lines[i].strip()
            if is_markdown_heading(lines[i]) or is_interaction_header(lines[i]):
                break

            if s:
                step_lines.append(lines[i].strip())
            i += 1

        new_lines.append("<details>")
        new_lines.append("<summary><strong>Show steps</strong></summary>")
        new_lines.append("")

        for step in step_lines:
            new_lines.append(f"- {step}")

        if step_lines:
            new_lines.append("")

        new_lines.append("</details>")
        new_lines.append("")
        count += 1

    if count > 0:
        click.echo(click.style("Detected reveal blocks", fg="blue"))
        click.echo(f"  Rendering {count} reveal interactions")

    return "\n".join(new_lines), count


def parse_quiz(content: str) -> tuple[str, int]:
    """
    Parse Word-authored Quiz blocks into a static formative quiz UI.
    """
    lines = content.split("\n")
    new_lines = []
    count = 0
    i = 0
    quiz_index = 0

    def esc(text: str) -> str:
        return (
            text.replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
                .replace('"', "&quot;")
        )

    while i < len(lines):
        stripped = lines[i].strip()

        if not re.match(r"^(?:#+\s*)?Quiz\s*$", stripped, re.IGNORECASE):
            new_lines.append(lines[i])
            i += 1
            continue

        question = ""
        options = []
        answer = ""
        explanation_lines = []
        i += 1
        quiz_index += 1
        quiz_name = f"quiz_{quiz_index}"

        while i < len(lines):
            s = lines[i].strip()

            if is_markdown_heading(lines[i]) or is_interaction_header(lines[i]):
                break

            q_match = re.match(r"^Question\s*::\s*(.*)$", s, re.IGNORECASE)
            o_match = re.match(r"^Option\s*::\s*(.*)$", s, re.IGNORECASE)
            a_match = re.match(r"^Answer\s*::\s*(.*)$", s, re.IGNORECASE)
            e_match = re.match(r"^Explanation\s*::\s*(.*)$", s, re.IGNORECASE)

            if q_match:
                question = q_match.group(1).strip()
            elif o_match:
                options.append(o_match.group(1).strip())
            elif a_match:
                answer = a_match.group(1).strip()
            elif e_match:
                explanation_lines.append(e_match.group(1).strip())
            elif s:
                explanation_lines.append(lines[i].strip())

            i += 1

        new_lines.append("")
        new_lines.append("## Quiz")
        new_lines.append("")

        if question:
            new_lines.append(question)
            new_lines.append("")

        if options:
            new_lines.append(f'<form class="quiz-block" data-quiz="{quiz_name}">')
            for idx, option in enumerate(options, start=1):
                option_id = f"{quiz_name}_opt_{idx}"
                option_html = esc(option)
                new_lines.append(
                    f'<div class="quiz-option">'
                    f'<input type="radio" id="{option_id}" name="{quiz_name}" value="{option_html}"> '
                    f'<label for="{option_id}">{option_html}</label>'
                    f'</div>'
                )
            new_lines.append("</form>")
            new_lines.append("")

        new_lines.append("<details>")
        new_lines.append("<summary><strong>Show answer</strong></summary>")
        new_lines.append("")

        if answer:
            new_lines.append(f"**Answer:** {esc(answer)}")
            new_lines.append("")

        if explanation_lines:
            new_lines.append("**Explanation:**")
            new_lines.append("")
            new_lines.append("\n".join(explanation_lines).strip())
            new_lines.append("")

        new_lines.append("</details>")
        new_lines.append("")
        count += 1

    if count > 0:
        click.echo(click.style("Detected quiz blocks", fg="blue"))
        click.echo(f"  Rendering {count} static single-select quizzes")

    return "\n".join(new_lines), count


def parse_images(content: str, qmd_path: Path, course_dir: Path) -> tuple[str, int]:
    lines = content.split("\n")
    new_lines = []
    count = 0
    i = 0

    while i < len(lines):
        stripped = lines[i].strip()
        match = re.match(r"^(?:#+\s*)?Image\s*::\s*(.+)$", stripped, re.IGNORECASE)

        if not match:
            new_lines.append(lines[i])
            i += 1
            continue

        raw_path = match.group(1).strip()
        path = rewrite_asset_path(raw_path, qmd_path, course_dir)
        alt = ""
        caption = ""
        width = ""
        i += 1

        while i < len(lines):
            s = lines[i].strip()
            if is_markdown_heading(lines[i]) or is_interaction_header(lines[i]):
                break

            alt_match = re.match(r"^Alt\s*::\s*(.*)$", s, re.IGNORECASE)
            cap_match = re.match(r"^Caption\s*::\s*(.*)$", s, re.IGNORECASE)
            width_match = re.match(r"^Width\s*::\s*(.*)$", s, re.IGNORECASE)

            if alt_match:
                alt = alt_match.group(1).strip()
            elif cap_match:
                caption = cap_match.group(1).strip()
            elif width_match:
                width = width_match.group(1).strip()

            i += 1

        image_line = f"![{alt}]({path})"
        if width:
            image_line += f"{{width='{width}'}}"

        new_lines.append(image_line)
        if caption:
            new_lines.append(caption)
        new_lines.append("")
        count += 1

    if count > 0:
        click.echo(click.style("Detected image blocks", fg="blue"))
        click.echo(f"  Rendering {count} images")

    return "\n".join(new_lines), count


def parse_files(content: str, qmd_path: Path, course_dir: Path) -> tuple[str, int]:
    lines = content.split("\n")
    new_lines = []
    count = 0
    i = 0

    while i < len(lines):
        stripped = lines[i].strip()
        match = re.match(r"^(?:#+\s*)?File\s*::\s*(.+)$", stripped, re.IGNORECASE)

        if not match:
            new_lines.append(lines[i])
            i += 1
            continue

        raw_path = match.group(1).strip()
        path = rewrite_asset_path(raw_path, qmd_path, course_dir)
        label = "Download file"
        display = ""
        i += 1

        while i < len(lines):
            s = lines[i].strip()
            if is_markdown_heading(lines[i]) or is_interaction_header(lines[i]):
                break

            label_match = re.match(r"^Label\s*::\s*(.*)$", s, re.IGNORECASE)
            display_match = re.match(r"^Display\s*::\s*(.*)$", s, re.IGNORECASE)

            if label_match:
                label = label_match.group(1).strip()
            elif display_match:
                display = display_match.group(1).strip().lower()

            i += 1

        if display == "embed" and path.lower().endswith(".pdf"):
            iframe_title = f"Embedded PDF: {label}" if label else "Embedded PDF document"
            new_lines.append(
                f'<iframe src="{path}" title="{iframe_title}" width="100%" height="600" loading="lazy"></iframe>'
            )
            new_lines.append("")
            new_lines.append(f"[{label}]({path})")
            new_lines.append("")
        else:
            new_lines.append(f"[{label}]({path})")
            new_lines.append("")

        count += 1

    if count > 0:
        click.echo(click.style("Detected file links", fg="blue"))
        click.echo(f"  Rendering {count} file links")

    return "\n".join(new_lines), count


def parse_embeds(content: str) -> tuple[str, int]:
    """
    Parse simple single-line embed directives:

    YouTubeEmbed :: <url>
    PanoptoEmbed :: <url>
    """
    lines = content.split("\n")
    new_lines = []
    count = 0

    for line in lines:
        stripped = line.strip()

        yt_match = re.match(r"^(?:#+\s*)?YouTubeEmbed\s*::\s*(.+)$", stripped, re.IGNORECASE)
        pan_match = re.match(r"^(?:#+\s*)?PanoptoEmbed\s*::\s*(.+)$", stripped, re.IGNORECASE)

        if yt_match:
            url = yt_match.group(1).strip()
            new_lines.append(render_youtube_iframe(url))
            new_lines.append("")
            count += 1
        elif pan_match:
            url = pan_match.group(1).strip()
            new_lines.append(render_panopto_iframe(url))
            new_lines.append("")
            count += 1
        else:
            new_lines.append(line)

    if count > 0:
        click.echo(click.style("Detected video embeds", fg="blue"))
        click.echo(f"  Rendering {count} YouTube/Panopto embeds")

    return "\n".join(new_lines), count


def parse_interactions(content: str, qmd_path: Path, course_dir: Path) -> str:
    """Coordinator function for parsing supported interaction types."""
    total_interactions = 0

    content = normalize_metadata_blocks(content)
    content = normalize_math_blocks(content)

    content, count = parse_tabs(content)
    total_interactions += count

    content, count = parse_r_example(content)
    total_interactions += count

    content, count = parse_r_code(content)
    total_interactions += count

    content, count = parse_callouts(content)
    total_interactions += count

    content, count = parse_selfcheck(content)
    total_interactions += count

    content, count = parse_reveal(content)
    total_interactions += count

    content, count = parse_quiz(content)
    total_interactions += count

    content, count = parse_images(content, qmd_path, course_dir)
    total_interactions += count

    content, count = parse_files(content, qmd_path, course_dir)
    total_interactions += count

    content, count = parse_embeds(content)
    total_interactions += count

    if total_interactions == 0:
        click.echo("  No interaction patterns detected")

    return content


def insert_markdown_into_qmd(md_path: Path, qmd_path: Path, course_dir: Path):
    """
    Inserts Markdown content into a QMD file.
    - Creates a .bak backup.
    - Uses IMPORT_START/END markers for idempotency.
    - If markers are missing, inserts after the frontmatter's second ---.
    """
    if not qmd_path.exists():
        raise FileNotFoundError(f"Target QMD file not found: {qmd_path}")

    with open(md_path, "r") as f:
        imported_content = f.read()

    imported_content = parse_interactions(imported_content, qmd_path, course_dir).strip()

    imported_content = re.sub(r"^\s*#\s+[^\n]*\n*", "", imported_content, count=1)
    imported_content = re.sub(r"^\s*Title:\s*[^\n]*\n*", "", imported_content, count=1, flags=re.IGNORECASE)
    imported_content = imported_content.strip()

    with open(qmd_path, "r") as f:
        qmd_content = f.read()

    backup_path = qmd_path.with_suffix(qmd_path.suffix + ".bak")
    shutil.copy2(qmd_path, backup_path)

    new_imported_block = f"\n\n{IMPORT_START}\n\n{imported_content}\n\n{IMPORT_END}\n"

    if IMPORT_START in qmd_content and IMPORT_END in qmd_content:
        pattern = re.escape(IMPORT_START) + r".*?" + re.escape(IMPORT_END)
        new_qmd_content = re.sub(
            pattern,
            f"{IMPORT_START}\n\n{imported_content}\n\n{IMPORT_END}",
            qmd_content,
            flags=re.DOTALL,
        )
    else:
        fm_pattern = r"^---\s*\n.*?\n---\s*\n"
        fm_match = re.search(fm_pattern, qmd_content, re.DOTALL)

        if fm_match:
            insert_pos = fm_match.end()
            new_qmd_content = qmd_content[:insert_pos] + new_imported_block + qmd_content[insert_pos:]
        else:
            new_qmd_content = new_imported_block + qmd_content

    with open(qmd_path, "w") as f:
        f.write(new_qmd_content)


def _iter_pages(config):
    """Yield all effective pages in module order."""
    for session in config.sessions:
        for section in session.sections:
            for page in section.effective_pages:
                yield session, section, page


def _find_target_qmd(course_dir: Path, page_id: str) -> Path | None:
    """Locate generated QMD file by page ID-derived filename."""
    target_qmd_name = f"{page_id}.qmd"
    for root, _, files in os.walk(course_dir):
        if target_qmd_name in files:
            return Path(root) / target_qmd_name
    return None


def run_import(config_path: str):
    """Orchestrates the import workflow using YAML-declared source_docx paths."""
    if not check_pandoc():
        click.echo(
            click.style("Pandoc is not installed. Please install Pandoc to use import-word.", fg="red"),
            err=True,
        )
        return

    try:
        config = ConfigLoader.load(config_path)
        course_id = config.module.id.lower()
        click.echo(f"Importing Word content for course: {course_id}")

        import_dir = Path("imports") / course_id
        md_dir = import_dir / "md"
        md_dir.mkdir(parents=True, exist_ok=True)

        course_dir = Path("course") / course_id
        if not course_dir.exists():
            parent = course_dir.parent
            options = [d for d in parent.iterdir() if d.is_dir() and d.name.startswith(course_id)] if parent.exists() else []
            if not options:
                click.echo(
                    click.style(f"Error: Course directory {course_dir} not found. Run 'build' first.", fg="red"),
                    err=True,
                )
                return
            course_dir = sorted(options)[-1]

        click.echo(f"Locating target files in: {course_dir}")

        copy_site_resources(course_dir)

        imported_count = 0
        skipped_count = 0

        for _, _, page in _iter_pages(config):
            if not getattr(page, "source_docx", None):
                skipped_count += 1
                click.echo(click.style(f"Skipping page '{page.id}' (no source_docx)", fg="yellow"))
                continue

            docx_path = Path(page.source_docx)

            if not docx_path.exists():
                skipped_count += 1
                click.echo(click.style(f"Warning: {docx_path} not found. Skipping page '{page.id}'.", fg="yellow"))
                continue

            md_path = md_dir / docx_path.with_suffix(".md").name

            click.echo(f"Converting {docx_path.name} to Markdown for page {page.id}")
            convert_docx_to_md(docx_path, md_path)
            click.echo(f"  Saved to {md_path}")

            with open(md_path, "r") as f:
                raw_md = f.read()

            warnings = validate_import_content(raw_md, page.id, project_root=Path("."))
            print_validation_warnings(warnings)

            target_path = _find_target_qmd(course_dir, page.id)
            if target_path:
                click.echo(f"Inserting converted content into {target_path}")
                insert_markdown_into_qmd(md_path, target_path, course_dir)
                imported_count += 1
            else:
                skipped_count += 1
                click.echo(
                    click.style(f"Error: Target QMD for page '{page.id}' not found in {course_dir}.", fg="red")
                )

        click.echo(click.style(f"✅ Import complete. Imported: {imported_count}, Skipped: {skipped_count}", fg="green"))

    except Exception as e:
        click.echo(click.style(f"Error: {str(e)}", fg="red"), err=True)