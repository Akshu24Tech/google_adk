# 🔍 Code Review Agent — Google ADK + Skills

A production-structured AI code reviewer built with **Google ADK's Skills system**. Demonstrates modular agent design using the `SkillToolset` pattern — each capability is an isolated, lazily-loaded skill.

## Why ADK Skills?

Traditional agents stuff ALL instructions into one giant system prompt. ADK Skills fix this:

- **L1 (Metadata):** Agent discovers skills via frontmatter — no context cost
- **L2 (Instructions):** Loaded only when the skill is triggered
- **L3 (Resources):** References/assets loaded on demand inside the skill

Result: Smaller operating context window, modular capabilities, easier maintenance.

---

## Project Structure

```
code-review-agent/
├── agent.py                          # Root agent definition
├── requirements.txt
├── .env.example
└── skills/
    ├── code-review-skill/            # General code quality review
    │   ├── SKILL.md                  # L1 metadata + L2 instructions
    │   ├── references/
    │   │   ├── review-checklist.md   # L3 resource
    │   │   └── output-format.md      # L3 resource
    │   └── assets/
    │       └── severity-guide.md     # L3 resource
    │
    ├── security-scan-skill/          # OWASP-based security scanning
    │   ├── SKILL.md
    │   ├── references/
    │   │   └── owasp-patterns.md
    │   └── assets/
    │       └── safe-vs-unsafe.md
    │
    └── complexity-skill/             # Cyclomatic/cognitive complexity
        ├── SKILL.md
        └── references/
            └── complexity-metrics.md
```

---

## Agent Capabilities

| Skill | Triggers when... | What it does |
|---|---|---|
| `code-review-skill` | General review request | Quality, naming, DRY, design checks |
| `security-scan-skill` | Security/vuln mentioned | OWASP Top 10 pattern detection |
| `complexity-skill` | Complexity/refactor asked | Cyclomatic complexity, nesting, length |

Plus two utility `FunctionTool`s:
- `detect_language` — heuristic language detection
- `count_lines` — code size stats (total/code/comment/blank)

---

## Setup

```bash
git clone <your-repo>
cd code-review-agent

python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate

pip install -r requirements.txt

cp .env.example .env
# Add your GOOGLE_API_KEY to .env
```

## Run

```bash
# ADK dev UI (recommended for testing)
adk web

# Or CLI
adk run agent.py
```

---

## Example Prompts

```
"Review this Python function for me: [paste code]"
"Do a full review of this — quality, security, and complexity"
"Any security issues in this code? [paste code]"
"This function feels too complex, can you analyze it?"
```

---

## Key Concepts Demonstrated

- **`SkillToolset`** — bundles multiple skills + additional tools in one toolset
- **`load_skill_from_dir`** — filesystem-based skill loading (L1/L2/L3 structure)
- **`FunctionTool`** — plain Python functions as agent tools alongside skills
- **Skill `references/` + `assets/`** — structured knowledge the skill reads on demand
- **Lazy loading** — skills don't bloat context until triggered

---

## Built With

- [Google ADK Python](https://github.com/google/adk-python) v1.25.0+
- [Agent Skills Specification](https://agentskills.io/specification)
- Gemini 2.0 Flash
