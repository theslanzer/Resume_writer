# from pathlib import Path
# from typing import Mapping, Any, Dict, List, Tuple, Optional
# import fitz  # PyMuPDF

# from .html_builder import build_html
# from .pdf import html_to_pdf_bytes
# import fitz

# def sanity_check_fonts(pdf_path: str | Path) -> set[tuple[str, bool]]:
#     with fitz.open(pdf_path) as doc:
#         return {(f[3], f[4]) for page in doc for f in page.get_fonts(full=True)}

# def render_pdf(
#     data,
#     out_path: str | Path,
#     company_name: str,
#     settings: Mapping[str, Any],
#     *,
#     ask_if_overflow: bool = True,
#     debug_dump: bool = False,
#     debug_dir: str | Path = "debug_attempts",
# ) -> Tuple[Path, List[Tuple[float, Dict[str, float]]]]:

#     start_font  = settings["start_font"]
#     min_font    = settings["min_font"]
#     max_font    = settings["max_font"]
#     font_step   = settings["font_step"]
#     margin_min  = settings["margin_min"]
#     margin_max  = settings["margin_max"]
#     margin_step = settings["margin_step"]

#     f: float = min(start_font, max_font)
#     m: Dict[str, float] = {k: margin_max for k in ("top", "bottom", "left", "right")}

#     debug_path: Optional[Path] = None
#     if debug_dump:
#         debug_path = Path(debug_dir)
#         debug_path.mkdir(parents=True, exist_ok=True)

#     full_name = ""
#     if getattr(data, "header", None) and data.header.first_name and data.header.last_name:
#         full_name = f"{data.header.first_name} {data.header.last_name}"

#     tried: List[Tuple[float, Dict[str, float]]] = []
#     attempt = 0
#     final_pdf: bytes = b""

#     while True:
#         attempt += 1
#         tried.append((f, m.copy()))

#         html = build_html(data, full_name, f, m)
#         pdf_bytes = html_to_pdf_bytes(html, m)

#         if debug_dump and debug_path:
#             fname = f"preview.pdf"
#             (debug_path / fname).write_bytes(pdf_bytes)

#         with fitz.open(stream=pdf_bytes, filetype="pdf") as doc:
#             pages = len(doc)

#         if pages <= 1:
#             final_pdf = pdf_bytes
#             break

#         if any(v > margin_min for v in m.values()):
#             for k in m:
#                 m[k] = max(margin_min, m[k] - margin_step)
#             continue

#         if f > min_font:
#             f = max(min_font, f - font_step)
#             m = {k: margin_max for k in m}  # reset margins
#             continue

#         if ask_if_overflow:
#             print(f"Content still spans {pages} pages at min settings.")
#             if input("Generate anyway? [y/N]: ").strip().lower() != "y":
#                 raise SystemExit("Aborted by user.")
#         final_pdf = pdf_bytes
#         break

#     out_path = Path(out_path)
#     out_path.parent.mkdir(parents=True, exist_ok=True)
#     out_path.write_bytes(final_pdf)
#     if debug_dump:
#         fonts = sanity_check_fonts(out_path)
#         print("Fonts in PDF:", fonts)
#     return out_path, tried


from pathlib import Path
from typing import Mapping, Any, Dict, List, Tuple, Optional
import fitz  # PyMuPDF

from .html_builder import build_html
from .pdf import html_to_pdf_bytes


def sanity_check_fonts(pdf_path: str | Path) -> set[tuple[str, bool]]:
    with fitz.open(pdf_path) as doc:
        return {(f[3], f[4]) for page in doc for f in page.get_fonts(full=True)}


def render_pdf(
    data,
    out_path: str | Path,
    company_name: str,
    settings: Mapping[str, Any],
    *,
    ask_if_overflow: bool = True,
    debug_dump: bool = False,
    debug_dir: str | Path = "debug_attempts",
) -> Tuple[Path, List[Tuple[float, Dict[str, float]]]]:

    # -------- settings ----------
    start_font = settings["start_font"]
    min_font   = settings["min_font"]
    max_font   = settings["max_font"]
    font_step  = settings["font_step"]

    s_max   = settings["base_margin_max"]
    s_min   = settings["base_margin_min"]
    offset  = settings["header_offset"]
    step    = settings["margin_step"]

    # -------- initial values ----------
    f: float = min(start_font, max_font)
    m: Dict[str, float] = {
        "left":  s_max,
        "right": s_max,
        "top":   s_max + offset,
        "bottom":s_max + offset,
    }

    debug_path: Optional[Path] = None
    if debug_dump:
        debug_path = Path(debug_dir)
        debug_path.mkdir(parents=True, exist_ok=True)

    full_name = ""
    if getattr(data, "header", None) and data.header.first_name and data.header.last_name:
        full_name = f"{data.header.first_name} {data.header.last_name}"

    tried: List[Tuple[float, Dict[str, float]]] = []
    attempt = 0
    final_pdf: bytes = b""

    # -------- fit loop ----------
    while True:
        attempt += 1
        tried.append((f, m.copy()))

        html = build_html(data, full_name, f, m)
        pdf_bytes = html_to_pdf_bytes(html, m)

        if debug_dump and debug_path:
            (debug_path / f"preview.pdf").write_bytes(pdf_bytes)

        with fitz.open(stream=pdf_bytes, filetype="pdf") as doc:
            pages = len(doc)

        if pages <= 1:
            final_pdf = pdf_bytes
            break

        # 1) shrink side margins
        shrunk = False
        for k in ("left", "right"):
            if m[k] > s_min:
                m[k] = max(s_min, m[k] - step)
                shrunk = True

        if shrunk:
            m["top"]    = m["left"] + offset
            m["bottom"] = m["right"] + offset
            continue

        # 2) shrink header/footer
        for k in ("top", "bottom"):
            if m[k] > s_min + offset:
                m[k] = max(s_min + offset, m[k] - step)
                shrunk = True

        if shrunk:
            continue

        # 3) shrink font
        if f > min_font:
            f = max(min_font, f - font_step)
            m = {"left": s_max, "right": s_max,
                 "top": s_max + offset, "bottom": s_max + offset}
            continue

        # 4) overflow
        if ask_if_overflow:
            print(f"Content still spans {pages} pages at min settings.")
            if input("Generate anyway? [y/N]: ").strip().lower() != "y":
                raise SystemExit("Aborted by user.")
        final_pdf = pdf_bytes
        break

    # -------- save & sanity check ----------
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(final_pdf)

    if debug_dump:
        fonts = sanity_check_fonts(out_path)
        print("Fonts in PDF:", fonts)

    return out_path, tried
