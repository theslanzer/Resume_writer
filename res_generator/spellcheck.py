# res_generator/spellcheck.py
from language_tool_python import LanguageTool, Match
from pathlib import Path
from typing import Iterable

_tool = LanguageTool("en-US")   # instantiate once

# CUSTOM_WORDS = [
#     "Shaswot",
#     "Joshi"
#     "LangChain",
#     "CrewAI",
#     "Plotly",
#     "dbt",
#     "Streamlit",
#     "Snowflake",
#     "Hex",          # BI tool, not the colour!
# ]

# _tool.wordfeq.add_words(CUSTOM_WORDS) 

def match_to_word(match: Match) -> str:
    """Extract the actual text LanguageTool marked as incorrect."""
    # match.offset and errorLength refer to the `context` string
    start = match.offset
    end   = match.offset + match.errorLength
    return match.context[start:end]

def check_text(text: str) -> list[tuple[str, str]]:
    """Return [(word, message), …] for a block of text."""
    problems = []
    for m in _tool.check(text):
        wrong = match_to_word(m)
        problems.append((wrong, m.message))
    return problems

def resume_iter_strings(data) -> Iterable[tuple[str, str]]:
    """
    Yield (location, string) pairs from the ResumeData object,
    e.g. ("experience[0].bullets[2]", "Reduced latency by 50% ...")
    """
    if data.header:
        for fld in ("first_name", "last_name", "address"):
            val = getattr(data.header, fld, None)
            if val:
                yield (f"header.{fld}", val)

    for i, exp in enumerate(data.experience or []):
        for j, b in enumerate(exp.bullets or []):
            yield (f"experience[{i}].bullets[{j}]", b)

    for i, proj in enumerate(data.projects or []):
        for j, b in enumerate(proj.bullets or []):
            yield (f"projects[{i}].bullets[{j}]", b)

    # add skills / education if desired …

def spellcheck_resume(data) -> list[tuple[str, str, str]]:
    """
    Return [(location, word, message), …]
    e.g. ("experience[0].bullets[2]", "analitics", "Possible spelling mistake…")
    """
    issues = []
    for loc, txt in resume_iter_strings(data):
        for word, msg in check_text(txt):
            issues.append((loc, word, msg))
    return issues
