# ArmorIQ: knowledge snapshot (Nov 2026)

From research of armoriq.ai, docs.armoriq.ai, their blog/Substack, GitHub and public sources. **Verify specifics against the live docs.** Items marked (self-reported) come from the company's own site.

## What ArmorIQ does (one paragraph)

ArmorIQ is an intent-enforcement layer for autonomous AI agents. It captures what an agent plans to do for a task, binds that plan cryptographically, and checks every action against the plan and the org's policy **before the action executes**: Allow, Hold (human approval) or Block. It is fail-closed: if no decision can be reached, the action is withheld. Motto: *"It's not about Identity. It's about Intent."* Positioning: *"Authenticated doesn't mean aligned."* An agent with valid credentials can still act outside its task, through prompt injection, intent drift or over-eager recovery. IAM answers *who*; ArmorIQ answers *whether this action belongs to this task*. It complements IAM, zero trust and monitoring rather than replacing them.

## Core concepts

- **Intent:** the task's purpose, treated as an *invariant* (Ketan's framing). Not the prompt, not the current plan, not the latest reasoning. The route can change; the goal can't.
- **Manifesto principles:** intent interception (see the plan before execution) · context enforcement (user identity, delegated scope, trust domain, policy) · policy-infused autonomy · complete auditability.
- **Related ideas:** intent-bound execution · scoped delegation (sub-agents get narrower, temporary authority) · purpose-aware governance (access expires when intent expires).
- **Lifecycle:** Discover (register agents and MCP servers, owners, org policy) → Enforce (sign the plan, verify each action) → Prove (tamper-evident audit log).
- **CSRG** (Canonical Structured Reasoning Graph): the plan normalised into a deterministic graph, so the same plan always hashes the same.
- **IAP** (Intent Assurance Plane): the cryptographic layer between reasoning and tool execution. "If a tool wasn't in the plan, it doesn't run."
- **Intent commit:** signed Merkle root over the CSRG. **Intent token:** carries `plan_hash`, `merkle_root`, `step_proofs`. Strict mode (`CSRG_VERIFY_ENABLED`, `REQUIRE_CSRG_PROOFS`) requires Merkle inclusion proofs on every invoke.
- **Deterministic:** the core check is plan membership plus rules, not a model judging. Claimed **< 5 ms p99** per policy decision.

## Products

| Layer | Product | Notes |
|---|---|---|
| Model API | **Intent Gateway** | Proxy at `gw.armoriq.ai`; change the SDK base URL; uses your own provider key |
| Application | **SDK** (Python, TypeScript) | `capture_plan` → `get_intent_token` → `invoke` |
| Dev workstation | **ArmorTools** | ArmorClaude, ArmorCodex, ArmorGemini, ArmorCopilot, ArmorOpenCode, ArmorClaw |
| OS / kernel | **Intent Container** | intentd, KAP, iVisor |
| Management | **Platform console** | platform.armoriq.ai |
| Vertical | ArmorPay / ArmorHealth / ArmorEdu | Domain policy packs |

### Intent Gateway

- `https://gw.armoriq.ai/v1/t/<gateway-key>`: **record only**.
- `…/v1/t/<gateway-key>/a/<agent-id>`: **record + enforce** that agent's active policy.
- Supports the OpenAI SDK (Chat Completions, streaming and non-streaming, tools), the Anthropic SDK (Messages, tool use), and Gemini via the OpenAI SDK. **Not** Claude via the OpenAI SDK.
- Outcomes: Allow · Block (call removed, note names the rule) · Hold (approval request created; *approving doesn't yet release the retry*) · Withhold (fail-closed).
- Limits: ~120 policy calls/min per gateway key; requests over 5 min are cut; enforcement needs a registered, active agent.
- Each tool-requesting response is recorded as a plan with a signed intent token, the same record the SDK produces.

### SDK (Python example from their docs, condensed)

```python
from armoriq_sdk import ArmorIQClient

client = ArmorIQClient()          # reads ARMORIQ_API_KEY
user = "alice@example.com"
plan = {"goal": "Fetch sales data and analyze Q4 performance",
        "steps": [{"action": "fetch_sales", "mcp": "data-mcp", "params": {"quarter": "Q4"}}]}
captured = client.capture_plan(llm="gpt-4", prompt="...Q4 performance", plan=plan)
token = client.get_intent_token(captured)
client.invoke("data-mcp", "fetch_sales", token, {"quarter": "Q4"}, user_email=user)  # allowed
client.invoke("data-mcp", "delete_all", token, {}, user_email=user)                   # blocked
```

- `client.for_user(email)`: per-user scope with enforcement, holds and approval waiting.
- `delegate`: listed, **not documented**.
- CLI `armoriq`: `login`, `init`, `validate`, `register`, `orgs`, `keys`, `status`, `logs`; config in `armoriq.yaml`.
- Adapters: Google ADK, LangChain, Strands (Py + TS), CrewAI (Py). Published Claude skill: `armoriq-iap`.
- SDK mode for vertical packs: `invokeWithPolicy()`.

### ArmorTools

- **ArmorClaude** (Claude Code): one-command install (`curl …install_armorclaude.sh | bash`); registers a plan per prompt; enforces policy on every tool call via **hooks** (e.g. PreToolUse); rules can allow, hold or block a tool, or lock a folder.
- **ArmorGemini:** Gemini CLI must declare intent before acting. **ArmorClaw** (OpenClaw) is the most-starred repo (~270 stars).
- Shared concepts: **the record** (ordered log of actions and what they touched) and **the say** (rules). Watch-only mode is available.

### Intent Container

- Binds each task to its authorising objective; enforces on **files, processes, network, IPC**, "from the request path down to the kernel". Child processes inherit limits; authority can change live (fail-closed from the next check); decisions are attributed to the objective and the authority version.
- **intentd:** a daemon tracking objectives, lineage and authority (runs on Google Agent Substrate). **KAP:** a Linux kernel subsystem; core object the **Intent Lineage Group**; enforced via kernel security hooks; **securityfs** is the control plane. **iVisor:** a userspace application kernel where the host kernel can't change (experimental).
- Runtimes: NVIDIA **OpenShell**: Available (`armoriq-openshell-middleware`, no agent changes) · Google Agent Substrate, Linux, Docker Sandboxes: Preview · Kubernetes, AWS Bedrock: Coming.
- Blog line: *"Execution state can travel backward. Authority cannot."* (Snapshots and resume must not resurrect revoked permissions.) Mid-Sep 2026: "the kernel now enforces these controls."

### Console and policies

- Modules: Registry · Intent Engine · Gatekeeper · Sentry · Auditor (tamper-evident logs mapped to SOC 2, GDPR, NIST).
- Policies: tool permissions, IP restrictions, time windows, rate limits. Authoring: Policy Builder (visual), Policy Studio (forms + live YAML), OPA engine.
- **ArmorPay:** amount thresholds, velocity limits, recipient validation; example AP, Finance and Payroll agents. ArmorHealth and ArmorEdu are announced.

## Team and company

- **Ram Shanmugam** (CEO): Georgia Tech alumnus; appOrbit (→ Cohesity), AutonomIQ (→ Sauce Labs); third company.
- **Ketan Bhardwaj** (CTO): Georgia Tech PhD (systems, 2016); co-led the Kernel Research Group's edge-computing research; secure edge papers (AirBox, SPX).
- **Vaibhav Bhosale** (Chief Scientist): IIT Bombay B.Tech CSE (2013–17); Georgia Tech MS/PhD advised by Ada Gavrilovska and Ketan; LEO satellite network research.
- San Francisco; 16 builders + 12 advisors (incl. Matthew Rosenquist, ex-Intel); Berkeley Xcelerator Spring 2026; open-core; onboarding the first 50 design partners; no public funding round.
- Traction (self-reported): 54K+ SDK installs, 10K+ agents in production, ~2.1M intent calls, ~1.28M actions verified.

## Competitors

- Governance: Zenity, Noma Security.
- Prompt firewalls: Lakera (Check Point), Prompt Security (SentinelOne), Aim (Cato), Lasso, Pillar.
- Runtime startups: Straiker, Capsule, Tenet, Asymptote Labs, Rein, Manifold, Ultra Security, CodeIntegrity, Operant.
- Sandboxes (partners): NVIDIA OpenShell, Docker, Google Agent Substrate.
- Agent identity (closest threat): Okta for AI Agents, Microsoft.
- Suites: Palo Alto Prisma AIRS, Cisco AI Defense.

## Known gaps (from their own docs, worth verifying hands-on)

- Gateway Hold: approval doesn't yet release the action.
- `delegate()` is undocumented.
- The policy-format reference and the ArmorCopilot / ArmorGemini pages are thin.
- Intent Container on Kubernetes and Bedrock: "Coming"; iVisor experimental.
- Open questions: plan validation (injection *before* planning) · re-planning agents (new token per re-plan? objective invariance without too many holds?) · public benchmarks · more end-to-end examples and case studies.

## Links

- Site: https://armoriq.ai · Docs: https://docs.armoriq.ai · Console: https://platform.armoriq.ai · GitHub: https://github.com/armoriq
- Gateway: https://docs.armoriq.ai/products/intent-gateway · Container: https://docs.armoriq.ai/products/intent-container · SDK: https://docs.armoriq.ai/sdk · Policies: https://docs.armoriq.ai/platform/policies · Tools: https://docs.armoriq.ai/tools · ArmorPay: https://docs.armoriq.ai/armorpay
- Manifesto: https://armoriq.ai/manifesto · Blog: https://armoriq.ai/blogs · Substack: https://armoriq.substack.com
