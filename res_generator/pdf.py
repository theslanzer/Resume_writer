from typing import Dict, cast
from playwright.sync_api import PdfMargins
from .playwright_pool import _BrowserPool
from .paths import STYLE_CSS
# from .fonts import inject_fonts_css

# TEMPLATE_DIR = Path(__file__).parent.parent / "templates" / "classic"

def html_to_pdf_bytes(html: str, margins: Dict[str, float]) -> bytes:
    page = _BrowserPool.page()
    page.set_content(html, wait_until="load")
    page.add_style_tag(path=str(STYLE_CSS.resolve()))
    # inject_fonts_css(page)

    pdf_margins: PdfMargins = cast(PdfMargins, {k: f"{v}in" for k, v in margins.items()})

    pdf_bytes = page.pdf(format="Letter", margin=pdf_margins, print_background=True)
    page.close()
    return cast(bytes, pdf_bytes)
