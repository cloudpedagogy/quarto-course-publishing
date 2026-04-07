import os
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

class PageKindResolver:
    """Resolves page kinds directly to QMD scaffolds in templates/pages/."""

    def __init__(self, templates_dir: str):
        self.templates_dir = Path(templates_dir)
        
        if not self.templates_dir.exists():
            # Create it if missing? For now, we expect it to exist if we're generating.
            # But the generator should handle this gracefully.
            pass

        self.env = Environment(
            loader=FileSystemLoader(str(self.templates_dir)),
            autoescape=False,
            trim_blocks=True,
            lstrip_blocks=True
        )

    def resolve_template(self, kind: str) -> str:
        """Returns the template filename for a given kind."""
        # Fallback to text_page if kind is missing
        if not kind:
            kind = "text_page"
            
        # Graceful mapping for standardized overview name
        if kind == "overview":
            kind = "overview_page"
            
        return f"{kind}.qmd"

    def render_scaffold(self, kind: str, context: dict = None) -> str:
        """Renders the scaffold for a given page kind if it exists."""
        template_name = self.resolve_template(kind)
        context = context or {}
        
        # Check if template exists
        if not (self.templates_dir / template_name).exists():
            # If the specific kind is missing, fallback to text_page.qmd
            if kind != "text_page":
                template_name = "text_page.qmd"
                if not (self.templates_dir / template_name).exists():
                    return "" # Total fallback if even text_page is missing
            else:
                return ""
        
        try:
            template = self.env.get_template(template_name)
            return template.render(**context).strip()
        except Exception as e:
            # We don't want to crash the whole build if one scaffold is buggy
            print(f"Warning: Error rendering scaffold for kind '{kind}': {str(e)}")
            return ""
