"""
resume_writer
=============

A tiny package that converts a JSON résumé into a single‑page, ATS‑friendly
PDF using Jinja templates and Playwright.
"""

from importlib.metadata import version, PackageNotFoundError
try:
    __version__ = version("res_generator")
except PackageNotFoundError:
    __version__ = "0.0.0"

__all__ = ["__version__"]

