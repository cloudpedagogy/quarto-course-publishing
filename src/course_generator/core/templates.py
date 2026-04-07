import jinja2
from pathlib import Path
from typing import Any, Dict

class TemplateManager:
    def __init__(self, templates_dir: str):
        self.templates_dir = Path(templates_dir)
        self.env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(str(self.templates_dir)),
            autoescape=False
        )

    def render(self, template_path: str, context: Dict[str, Any]) -> str:
        template = self.env.get_template(template_path)
        return template.render(**context)
