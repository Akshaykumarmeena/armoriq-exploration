# ArmorIQ: hands-on exploration + demo

## Who I am and why this project exists

I'm Akshay, a software engineer (intern at an AI startup, Python/Django stack) getting back into hands-on engineering and learning "Claude engineering" (Claude Code, skills, hooks, MCP). I've had calls with ArmorIQ's founders: Ram Shanmugam (CEO), Ketan Bhardwaj (CTO) and Vaibhav Bhosale (Chief Scientist). I'm preparing for a follow-up meeting where I need to:

1. Show I deeply understand what ArmorIQ does, from actually using it, not just reading about it.
2. Point out gaps and improvements, kindly and with evidence.
3. Show how I could contribute, ideally with a **small working demo I built**.

**The meeting is tomorrow.** Time matters: favour working, demonstrable progress over completeness.

Background knowledge is in `ARMORIQ_KNOWLEDGE.md`: products, SDK, terms, team, competitors and known gaps. Read it at the start of a session. Treat it as a snapshot from Nov 2026 research. Their docs may have changed, so verify against https://docs.armoriq.ai before relying on any specific API detail.

## Goals (in order)

1. **Learn by doing.** Try each product hands-on: sign up, get an API key, use the Python SDK, try the Intent Gateway, try the ArmorClaude plugin for Claude Code, explore the console.
2. **Keep a learning log** in `notes/LEARNING_LOG.md`: what I tried, what worked, what broke, what surprised me, with exact commands and errors. This is raw material for the meeting.
3. **Collect gaps and friction** in `notes/GAPS.md`: doc gaps, confusing steps, bugs, missing features. For each item, record what I expected, what happened, and a suggested fix. Be specific and fair.
4. **Pick and build one small demo** (decided together after exploring; see "Choosing the demo").
5. **Prepare a short meeting script** in `notes/MEETING.md`: a 2-minute demo walkthrough, 3–4 gaps framed as *"I noticed… / How are you thinking about…? / I'd love to help with…"*, and 1–2 concrete contribution offers.

## How I want you to work with me

- I'm learning. When something new comes up (a concept, a security idea, a kernel term, a crypto term), **explain it briefly in simple words** before or while using it.
- Prefer small steps I can run and see. Tell me what each command does before running anything that installs software or changes my system.
- **Python** is the main language (use a virtualenv, `requirements.txt`, Python 3.11+). TypeScript only if a tool requires it.
- Keep a clean repo: `README.md` (what this is, how to run it), `src/`, `notes/`, `.env.example`.
- After each milestone, update the learning log and suggest the next step.
- If ArmorIQ's docs and real behaviour differ, note it in `GAPS.md`. That's valuable for the meeting.

## Safety rules (important)

- **Never commit secrets.** API keys go in `.env` (git-ignored). Use `.env.example` with placeholders.
- ArmorClaude installs via `curl … | bash`. **Download and show me the script first**, explain what it does, and only run it after I agree.
- **ArmorClaude hooks into Claude Code itself**, so it may start governing *this* session (blocking or holding your tool calls). That's expected and interesting: if an action gets blocked or held, stop, tell me which rule triggered, and log it. Don't try to work around it.
- Don't run destructive or credential-touching commands to "test" blocking on my real files. Create a sandbox folder (e.g. `playground/`) with fake secrets like `playground/fake_credentials.txt` for demos.
- Don't sign up for accounts, accept terms, or push to GitHub on my behalf. Tell me the step and I'll do it.

## Exploration plan (suggested order)

1. **Setup:** create the repo structure, virtualenv, `.gitignore`, `.env.example`. I sign up at https://platform.armoriq.ai and get an API key. (Optional: I create a GitHub repo for this project.)
2. **Read the docs together:** https://docs.armoriq.ai (Overview, SDK, Intent Gateway, Intent Container, Policies, Tools, ArmorPay). Summarise anything that differs from `ARMORIQ_KNOWLEDGE.md`.
3. **SDK hello world:** install the Python SDK, reproduce their `capture_plan → get_intent_token → invoke` example. Show one allowed call and one blocked call (an action not in the plan).
4. **Intent Gateway:** point an OpenAI or Anthropic SDK client at `gw.armoriq.ai` in record-only mode, then enforce mode. Observe allow / block / hold.
5. **Console:** register an agent, write a policy in Policy Studio (look at the YAML), check the audit logs and observability for the calls above.
6. **ArmorClaude:** review the install script, install it, give Claude Code a small task in `playground/`, and watch the record and rules (e.g. lock a folder, block reading fake secrets).
7. **Skim** the GitHub org https://github.com/armoriq (ArmorClaw, ArmorGemini, SDKs) to understand the code structure.

## Choosing the demo

After steps 3–6, propose 2–3 demo options and help me pick one I can finish in a few hours. Criteria: works end to end, under 3 minutes to show, clearly shows ArmorIQ's value (**an action blocked because it wasn't in the signed plan, even with valid credentials**), and maps to a real contribution. Candidates:

- **Prompt-injection test kit:** a small agent reading "poisoned" inputs (email, web page, doc), plus a scenario runner that reports which injected actions ArmorIQ blocked. Could seed public benchmarks, a gap I want to raise.
- **Mini finance agent (ArmorPay style):** a "summarize vendor emails" agent where a hidden invoice-payment instruction gets blocked, plus amount, velocity and recipient rules.
- **Claude Code + ArmorClaude walkthrough:** a scripted coding task where reading fake credentials or force-pushing gets blocked or held.
- **Framework or web adapter:** e.g. a minimal Django or FastAPI integration example, if their adapters don't cover it.

## Definition of done for tomorrow

- [ ] I've used the SDK, Gateway, console and ArmorClaude at least once each.
- [ ] `notes/LEARNING_LOG.md` and `notes/GAPS.md` have real, specific entries.
- [ ] One demo runs from a clean checkout with `README.md` instructions.
- [ ] `notes/MEETING.md` has the walkthrough, the gaps and the contribution offers.
