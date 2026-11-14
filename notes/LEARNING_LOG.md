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

## 2026-11-13: Step 3, SDK hello world (part 1: before registering an agent)

Script: `src/hello_sdk.py`. Run with `.venv/bin/python src/hello_sdk.py`.

**Attempt 1: the docs quickstart as written** (`capture_plan` → `get_intent_token` → `invoke` on `weather-mcp`)
- `capture_plan` and `get_intent_token` worked: ArmorIQ returned a signed token (`plan_hash`, signature, expiry). **So my API key is valid.**
- Inside the token, `policy_validation` already said: `validated: False`, `denied_tools: ['get_weather']`, `reason: agent_unresolved`.
- Both `invoke` calls (the planned `get_weather` and the unplanned `send_email`) failed the same way:
  `MCPInvocationException: ... https://proxy.armoriq.ai/invoke (HTTP 500): 'Internal Proxy Error'`.
  So the "blocked" call and the "allowed" call looked identical. No clean "not in plan" message.

**Attempt 2: the session API** (`client.for_user(email).start_session()` → `start_plan` → `check`)
- First error: `ValueError: Tool "get_weather" is not namespaced as <MCP>__<action> and no default_mcp_name was set`. Tool names must be `weather-mcp__get_weather`.
- Then:
  ```
  weather-mcp__get_weather  -> BLOCK  reason: agent_unresolved: pass agent_id (or set AGENT_ID) to decide calls in local mode
  weather-mcp__send_email   -> BLOCK  reason: tool-not-in-plan: 'weather-mcp__send_email' was not declared in the captured plan
  ```
- **The core idea works:** the unplanned `send_email` is refused with a clear reason, even though my API key is valid.
- But the planned call is also refused, because no agent is registered. Fail-closed, which is correct security behaviour, but surprising after docs that say "no user/agent IDs to manage".

**Learned:** the SDK needs an agent registered in the console (and its id passed as `agent_id` / `AGENT_ID`) before anything is allowed.

- Next: register an agent in the console, put its id in `.env` as `ARMORIQ_AGENT_ID`, re-run.

## 2026-11-13: Step 3, part 2: registering an agent

- Console → Inventory → Agents → Add AI agent, Manual method. **Register failed:** `url must be a URL address. url should not be empty`, although the wizard says manual agents need no URL (GAPS #14). Workaround: the URL-based method with `https://example.com` → agent `hello-weather-agent` registered.
- Put the console's agent UUID in `.env` → still `agent_unresolved: no registered agent matches '<uuid>'`.
- Tried `agent_id="hello-weather-agent"` (the name) → resolved. New reason: `no_active_policy`, planned call still blocked (GAPS #15, #16).
- Learned: the SDK is deny-by-default. To allow anything you need: a registered agent (by name) **and** an active policy **and** the action in the signed plan. Three locks, all must open.
- CLI `armoriq policy templates` lists ready policies (all-allow, strict-read-only, balanced, lockdown…), but `policy show/set` needs `armoriq login`.

## 2026-11-14: Step 3, part 3: it works

- Policy Studio form wouldn't activate ("At least one governed tool is required"; agent had "No tools yet"). Wrote the rule by hand in the **YAML** tab:
  ```yaml
  spec:
    tools:
      default: block
      rules:
        get_weather: allow
  ```
  Activated fine.
- Re-ran `ARMORIQ_AGENT_ID=hello-weather-agent .venv/bin/python src/hello_sdk.py`:
  ```
  1. Plan signed: ... server policy check: validated=True reason=None
  weather-mcp__get_weather  -> ALLOWED  reason: allow:get_weather#0
  weather-mcp__send_email   -> BLOCK    reason: tool-not-in-plan: 'weather-mcp__send_email' was not declared in the captured plan
  ```
- **This is the core ArmorIQ idea working end to end:** same API key, same agent, same user. The planned action is allowed by policy rule `allow:get_weather#0`; the unplanned one is refused because it isn't in the signed plan.
- Policy rules key on the bare action name (`get_weather`), while the session API wants `<mcp>__<action>` (`weather-mcp__get_weather`).
- Getting here from a fresh account took ~6 workarounds (GAPS #9–#20). Time from signup to first "allowed": about one evening.
