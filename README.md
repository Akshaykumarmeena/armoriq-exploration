# ArmorIQ hands-on exploration

Hands-on notes and a small demo built while learning [ArmorIQ](https://armoriq.ai), an intent-enforcement layer for AI agents: it checks every agent action against a signed plan and policy before it runs (Allow / Hold / Block).

## Layout

| Path | What's there |
|---|---|
| `src/` | Python scripts: SDK hello world, gateway tests, the demo |
| `notes/LEARNING_LOG.md` | What I tried, what worked, what broke |
| `notes/GAPS.md` | Doc gaps, friction and bugs, each with a suggested fix |
| `notes/MEETING.md` | Demo walkthrough and talking points |
| `playground/` | Sandbox with **fake** secrets for blocking demos |
| `ARMORIQ_KNOWLEDGE.md` | Background research snapshot (Nov 2026) |

## Setup

Requires Python 3.10–3.13 (the SDK doesn't support 3.14 yet).

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # then put your ArmorIQ API key in .env
python src/check_setup.py
```

Get an API key at https://platform.armoriq.ai. Never commit `.env`.
