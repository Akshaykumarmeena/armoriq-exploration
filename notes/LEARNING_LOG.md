# Learning log

Raw notes: what I tried, exact commands, what happened, what surprised me.

## 2026-11-13: Step 1, setup

- Signed up at platform.armoriq.ai with my personal GitHub account; created an SDK API key (72 chars) and put it in `.env`.
- Repo set up: git, `.venv` (Python 3.13.15), `armoriq-sdk==0.8.18` from PyPI (supports Python >=3.10,<3.14).
- `python src/check_setup.py` → SDK imports, key loads, `ArmorIQClient()` constructs. Not yet proven that the server accepts the key (first real call is step 3).

## 2026-11-13: Step 2, reading the live docs

How I read them: the docs site is agent-friendly. `https://docs.armoriq.ai/llms.txt` is an index of ~297 pages, `/llms-full.txt` is the whole corpus (1.3 MB), and `/llms.mdx/<path>` gives one page as raw markdown. Nice touch, worth complimenting.

Then I checked the installed SDK against the docs:

```bash
.venv/bin/armoriq --help
.venv/bin/python -c "import inspect, armoriq_sdk as a; print(inspect.signature(a.ArmorIQClient.invoke))"
```

### What changed since my knowledge snapshot (ARMORIQ_KNOWLEDGE.md)

| Topic | Snapshot said | Live docs / real SDK say |
|---|---|---|
| `delegate()` | Listed, not documented | **Now documented** (`/sdk/core-methods/delegate`): Ed25519 public key of the sub-agent, `validity_seconds`, `allowed_actions`, chains of delegation. |
| Gateway Monitor mode | Not mentioned | **New.** Org-wide switch: every call is checked and the verdict recorded, nothing stopped; a "What policy would have done" 7-day report. Applies within ~90 s. |
| ArmorTools console | Assumed platform.armoriq.ai | **Separate console and account** at `tools.armoriq.ai`. One workspace per account, no teams, Free / Pro ($9/mo). Installer writes `~/.armoriq/credentials.json` after a device-code approval in the browser. |
| ArmorClaude install | `curl … \| bash` | `curl -fsSL https://armoriq.ai/install_armorclaude.sh \| bash` (ArmorCodex: `install_armorcodex.sh`). |
| Integrations | ADK, LangChain, Strands, CrewAI | Plus **Langflow** (via the `[langchain]` extra). `[openai]` and `[anthropic]` extras exist but "neither adapter is implemented". |
| ArmorHealth | Announced | Has docs pages and its own Policy Studio. |
| CLI | `login, init, validate, register, orgs, keys, status, logs` | Real 0.8.18 CLI also has `logout, whoami, switch-org, policy`. `switch-org` mints a new API key. |
| SDK internals | — | Default intent-token validity is **60 seconds** (`get_intent_token(validity_seconds=60.0)`). SDK also has `reanchor()` ("re-anchor a changed plan onto the token's plan") and `refine()` ("plan-assurance refinement, fails closed"): looks like their answer to the re-planning question. |
| API keys | — | Max 10 active keys per org; expiry 1 day / 7 / 30 / never; shown once. |

Everything else matched: gateway URLs and record vs enforce, verdicts, 120 policy calls/min, 5-minute cutoff, hold-doesn't-release, Intent Container layers and platform status table, ArmorPay agents and `invokeWithPolicy()`.

### Surprised by

- Two consoles (platform vs tools) with separate sign-ups. Need to check in step 6 whether my platform account works at tools.armoriq.ai.
- The Tools "Limits" page is unusually honest ("here is what is not built"). Good tone to mention in the meeting.
- Intent tokens live 60 s by default: long-running agents must re-mint often.

- Next: step 3, SDK hello world (one allowed call, one blocked call).
