"""
Code Review Agent — Built with Google ADK Skills
"""

import sys
import os

# Force UTF-8 everywhere on Windows (needed for emoji in SKILL.md files)
if sys.platform == "win32":
    os.environ.setdefault("PYTHONUTF8", "1")
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")

import pathlib
from google.adk import Agent
from google.adk.skills import load_skill_from_dir
from google.adk.tools import skill_toolset, FunctionTool

# ── Paths ──────────────────────────────────────────────────────────────────
SKILLS_DIR = pathlib.Path(__file__).parent / "skills"

# ── Load Skills ───────
code_review_skill = load_skill_from_dir(SKILLS_DIR / "code-review-skill")
security_scan_skill = load_skill_from_dir(SKILLS_DIR / "security-scan-skill")
complexity_skill = load_skill_from_dir(SKILLS_DIR / "complexity-skill")

# ── Custom Tools (non-skill utilities) ────────────────────────────────────\

def detect_language(code: str) -> dict:
    """
    Heuristic language detection from code snippet.
    In production, swap with pygments or linguist.
    """
    code_lower = code.lower()
    if "def " in code and "import " in code:
        return {"language": "Python", "confidence": "high"}
    elif "function " in code or "const " in code or "=>" in code:
        return {"language": "JavaScript/TypeScript", "confidence": "high"}
    elif "public class" in code or "void main" in code:
        return {"language": "Java", "confidence": "high"}
    elif "#include" in code or "std::" in code:
        return {"language": "C++", "confidence": "high"}
    else:
        return {"language": "Unknown", "confidence": "low"}


def count_lines(code: str) -> dict:
    """Returns line count stats for the submitted code."""
    lines = code.splitlines()
    non_empty = [l for l in lines if l.strip()]
    comment_lines = [l for l in lines if l.strip().startswith(("#", "//", "/*", "*"))]
    return {
        "total_lines": len(lines),
        "code_lines": len(non_empty) - len(comment_lines),
        "comment_lines": len(comment_lines),
        "blank_lines": len(lines) - len(non_empty),
    }


detect_language_tool = FunctionTool(detect_language)
count_lines_tool = FunctionTool(count_lines)

# ── Skill Toolset — bundles all 3 skills + utility tools ──────────────────
my_skill_toolset = skill_toolset.SkillToolset(
    skills=[
        code_review_skill,
        security_scan_skill,
        complexity_skill,
    ],
    additional_tools=[
        detect_language_tool,
        count_lines_tool,
    ],
)

# ── Root Agent ─────────────────────────────────────────────────────────────
root_agent = Agent(
    model="gemini-2.5-flash",
    name="code_review_agent",
    description=(
        "A senior-level AI code reviewer that analyzes code for quality, "
        "security vulnerabilities, and complexity. Provides structured, "
        "actionable feedback with severity labels."
    ),
    instruction="""
You are a senior software engineer and code reviewer with 10+ years of experience.

When the user submits code for review, follow this workflow:

1. Use `detect_language` tool to identify the programming language.
2. Use `count_lines` tool to get code size stats.
3. Decide which skills to invoke based on the request:
   - For general review → trigger `code-review-skill`
   - For security concerns → trigger `security-scan-skill`
   - For complexity/refactoring → trigger `complexity-skill`
   - If user says "full review" → run ALL THREE skills sequentially
4. Combine the outputs into one clean, well-structured report.

Always be specific, direct, and constructive. Never give vague feedback like
"this could be better" — always say exactly what and why.

If the user asks a general question about code review best practices,
answer from your expertise without invoking a skill.
""",
    tools=[my_skill_toolset],
)
