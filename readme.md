# Résumé / CV PDF Generator 📄⚡️

Python toolchain that turns a **single JSON file** into a **one-page, ATS-friendly PDF** using:

* **Jinja2** – HTML templating  
* **Playwright (Chromium)** – prints HTML to PDF (no wkhtml hassles)  
* **PyMuPDF (fitz)** – page-count detection  
* **Base64-embedded fonts** – razor-sharp Libertinus Serif on any device  

---

## ✨ Key Features
| Capability | Notes |
|------------|-------|
| 1-page auto-fit | Shrinks side margins → header/footer → font size until content fits A4. |
| Config-driven | All tunables (margins, font steps…) live in `settings.toml`. |
| Font embedding | OTFs in `/fonts/` are Base64-injected & embedded; no fallback blurs. |
| Multiple templates | Each template has its own `template.html`, `style.css`, `fonts.css`. |
| Batch-ready | A single Playwright browser is reused across renders ⇒ ~4× faster. |
| Debug previews | `--debug` dumps every fit attempt to `debug_attempts/`. |
| Typed schema | JSON validated with Pydantic (`schema.py`). |

---

## 🗂️ Folder Structure
```cpp
resume_writer/ ← Python package
│ cli.py ← command-line entry
│ renderer.py ← fit loop
│ html_builder.py ← Jinja renderer
│ pdf.py ← HTML → PDF
│ fonts.py ← inject Base64 fonts
│ playwright_pool.py ← keeps one Chromium
│ schema.py ← Pydantic models
│ ...
├─ templates/
│ └─ classic/
│ ├─ template.html
│ ├─ style.css
│ └─ fonts.css
├─ fonts/
│ └─ libertinus-serif/
│ ├─ LibertinusSerif-Regular.otf
│ └─ LibertinusSerif-Bold.otf
├─ settings.toml ← single source of truth
├─ sample_input.json
└─ README.md
```

---

## 🚀 Quick Start

```bash
# 1) set up venv
python -m venv .venv && . .venv/Scripts/activate  # Win: .venv\Scripts\activate

# 2) install deps
pip install -r requirements.txt
python -m playwright install chromium

# 3) generate your first PDF
python -m res_generator.cli -i sample_input.json -co parafin --debug-dump

Output lands in C:/Documents/Generated Resumes (see settings.toml).
```
---

## ⚙️ settings.toml

```toml
# font + margin fitting
start_font        = 11.0
min_font          = 8.0
max_font          = 11.0
font_step         = 0.5

side_margin_max   = 0.50   # L / R
side_margin_min   = 0.25
header_offset     = 0.25   # TOP = side + offset
margin_step       = 0.05

# paths
output_dir        = "C:/Documents/Generated Resumes"
debug_dir         = "debug_attempts"
```

---

## 📝 JSON Schema (snapshot)

```jsonc
{
  "header": {
    "first_name": "Jane",
    "last_name":  "Doe",
    "phone":      "+1 555 123 4567",
    "email":      "jane.doe@example.com",
    "linkedin":   "https://linkedin.com/in/janedoe"
  },
  "experience": [
    {
      "role":       "Data Analyst",
      "company":    "Acme Corp",
      "location":   "NY, USA",
      "start_date": "Jan 2021",
      "end_date":   "Present",
      "bullets": [
        "Built 14 Power BI dashboards",
        "Automated SQL pipelines → 40 % refresh time drop"
      ]
    }
  ],
  "projects": [...],
  "skills":   {...},
  "education": [...]
}

```
Full rules live in `schema.py`.

---

## 🖋️ Customising Templates / Fonts
1. New template
```cpp
templates/
  └─ modern/
      ├─ template.html
      ├─ style.css
      └─ fonts.css
```
Call: python -m resume_writer.cli ... --template modern.
2. Change fonts: Drop OTFs in /fonts/<family>/ → update paths in fonts.py.
Remember to stick to real weights (400 / 700 etc.).

---

## 🐛 Debugging
- `--debug` → saves every attempt (`debug_attempts/preview.pdf` …).
- `--verbose` → DEBUG-level logs (see margin/font values).

---

## 📜 License
MIT — do anything, just keep the notice.

---

## Acknowledgements

- Playwright – headless Chromium magic
- Libertinus Serif – SIL Open Font License
- Stack Overflow folks for print-CSS tricks

> Enjoy building résumé PDFs! Open issues and PRs welcomed.