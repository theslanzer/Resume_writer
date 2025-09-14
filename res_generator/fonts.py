from pathlib import Path
from playwright.sync_api import Page
from .paths import FONTS_DIR

def inject_libertinus(page: Page) -> None:
    regular = (FONTS_DIR / "LibertinusSerif-Regular.otf").as_uri()
    bold    = (FONTS_DIR / "LibertinusSerif-Bold.otf").as_uri()

    css = f"""
    @font-face {{
      font-family: "Libertinus Serif";
      src: url("{regular}") format("opentype");
      font-weight: 400;
      font-style: normal;
    }}
    @font-face {{
      font-family: "Libertinus Serif";
      src: url("{bold}") format("opentype");
      font-weight: 700;
      font-style: normal;
    }}
    html, body {{
      font-family: "Libertinus Serif", serif;
      font-weight: 400;
      font-synthesis: none;
      -webkit-font-smoothing: antialiased;
    }}
    """
    page.add_style_tag(content=css)
