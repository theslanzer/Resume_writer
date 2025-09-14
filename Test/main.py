import json
import click
from datetime import datetime
from pathlib import Path
from res_generator.schema import ResumeData
from res_generator.renderer import render_pdf
from res_generator.playwright_pool import _BrowserPool
from res_generator.config import load as load_cfg



@click.command()
@click.option("--input", "-i", type=click.Path(exists=True), required=True,
              help="Path to JSON resume data.")
@click.option("--outdir", "-o", type=click.Path(file_okay=False), default="D:/Documents/Generated Resumes",
              help="Output directory (will be created).")
@click.option("--company", "-co", default=None,
              help="Company name for file naming. If omitted, you'll be prompted.")
@click.option("--debug-dump", is_flag=True, default=False,
              help="Save every attempt PDF to ./debug_attempts")
@click.option("--debug-dir", default="debug_attempts",
              help="Directory for attempt PDFs")
@click.option("--config", "-c", default="settings.toml",
              type=click.Path(exists=True),
              help="Path to TOML settings file")

def main(config, input, outdir, company, debug_dump, debug_dir):
    # Initialize config
    cfg = load_cfg(config)

    # Load JSON
    data_dict = json.load(open(input, "r", encoding="utf-8"))

    # Validate
    data = ResumeData.model_validate(data_dict)

    # Skip null sections automatically handled via Jinja
    if company is None:
        company = click.prompt("Target company name", type=str)

    # Build filename
    first = (data.header.first_name if data.header and data.header.first_name else "first")
    last  = (data.header.last_name if data.header and data.header.last_name else "last")
    today = datetime.now().strftime("%d-%m-%Y")
    outfile = f"{first}_{last}_{company}_{today}.pdf"
    outdir = Path(cfg["paths"]["output_dir"])
    outdir.mkdir(parents=True, exist_ok=True)
    out_path = outdir / outfile

    # Run Renderer
    pdf_path, tried = render_pdf(data, 
                                out_path, 
                                company_name=company,
                                settings=cfg["defaults"], 
                                debug_dump=debug_dump, 
                                debug_dir=debug_dir)

    click.echo(f"Generated: {pdf_path}")
    # Optionally log the attempts:
    for fsize, margins in tried:
        click.echo(f"Tried font={fsize}, margins={margins}")
    _BrowserPool.close()

if __name__ == "__main__":
    main()