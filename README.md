# Teacher Assessment Forge

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE) [![AI Skill](https://img.shields.io/badge/AI-Skill-0f766e)](https://github.com/qasimrazamalik-coder/teacher-assessment-forge)

![Workflow](assets/workflow-preview.svg)

Create balanced assessment blueprints from learning objectives, difficulty targets and marking constraints.

Portable skill for Claude Code, Codex, ChatGPT, Claude, Gemini, Grok and custom MCP/agent runtimes. It combines concise agent instructions with an offline deterministic runner.

## Quick start

```bash
python skill/scripts/run.py examples/input.json
pytest -q
```

## Install

Copy `skill/` into your agent project or skills directory. For Claude Code or Gemini/Grok projects, reference `skill/SKILL.md` as project instructions and expose the runner as a local tool. No API key or third-party dependency is required.

## Responsible use

Use only authorized exports, official APIs or user-supplied data. This project does not bypass login, anti-bot controls, rate limits or privacy settings. See [Guardrails](docs/GUARDRAILS.md).

## Repository map

- `skill/` — installable, token-efficient capability
- `examples/` — reproducible demonstration
- `tests/` — executable contract test
- `docs/` — installation and guardrails

## Common questions

### What is Teacher Assessment Forge?

Teacher Assessment Forge provides a deterministic, provider-neutral AI workflow.

### Which AI tools can use it?

Claude Code, Codex, ChatGPT, Gemini, Grok, MCP-compatible agents, and custom agent runtimes can use the instructions and deterministic runner.

### Does it require an API key or cloud service?

No. The reference workflow runs locally with Python and uses no external dependency or network call.

### Is commercial use allowed?

Yes. The project is released under the permissive [MIT License](LICENSE), including commercial use, modification, and redistribution subject to the license notice.

### Where are the installation and safety instructions?

See [Installation](docs/INSTALLATION.md), [Guardrails](docs/GUARDRAILS.md), and [Security](SECURITY.md).

## Discovery keywords

teacher, assessment, forge, AI agent skill, agentic workflow, Claude Code skill, Codex skill, ChatGPT skill, Gemini skill, Grok skill, MCP, Python automation, open source AI tooling

## License

MIT © 2026 Qasim Raza Malik. See [LICENSE](LICENSE).
