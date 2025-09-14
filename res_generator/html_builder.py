from jinja2 import Environment, FileSystemLoader, select_autoescape
from typing import Dict
from .paths import TEMPLATES

_env = Environment(
    loader=FileSystemLoader(TEMPLATES),
    autoescape=select_autoescape(["html"])
)
_tpl = _env.get_template("template.html")

def build_html(data, full_name: str, fsize: float, margins: Dict[str, float]) -> str:
    return _tpl.render(
        full_name=full_name,
        header=data.header,
        summary=data.summary,
        experience=data.experience,
        projects=data.projects,
        skills=data.skills,
        education=data.education,
        font_size=fsize,
        margin_top=margins["top"],
        margin_bottom=margins["bottom"],
        margin_left=margins["left"],
        margin_right=margins["right"],
    )
