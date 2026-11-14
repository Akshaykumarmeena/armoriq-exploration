# Meeting script (2026-11-14)

Open with one line: *"I didn't just read the docs. I used the SDK, the Gateway and ArmorClaude, hit real blocks, and wrote down where I got stuck."*

Visual aid: the interactive page **ArmorIQ Field Notes** (https://claude.ai/artifact/JCQRha1wxdyYJ5Vjj8UVcS), the three-locks simulator works well live.

## 2-minute demo walkthrough

1. **The idea in one line (15 s).** "Authenticated isn't aligned." My API key is valid, my agent is registered, and ArmorIQ still blocks an action that wasn't in the signed plan.
2. **SDK (30 s).** Run `.venv/bin/python src/hello_sdk.py`:
   ```
   weather-mcp__get_weather  -> ALLOWED  allow:get_weather#0
   weather-mcp__send_email   -> BLOCK    tool-not-in-plan
   ```
   Same key, same agent, same user. Three locks must all open: agent known, policy allows the tool, action in the plan.
3. **Gateway (30 s).** Run `.venv/bin/python src/gateway_test.py --tricked --record`, then without `--record`:
   ```
   record:  get_weather ✓   send_email ✓
   enforce: get_weather ✓   send_email ✗  "blocked by policy: block:tools.default"
   ```
   Zero ArmorIQ code in the app, only a different base URL. Free Gemini key. The smoothest product I tried.
4. **ArmorClaude (30 s).** In Claude Code: `/armorclaude:armor policy add allow Read and Grep and Glob, deny Write and Edit, hold Bash` → `Write(hello.txt)` blocked (`policy forbid: policy4`) **even though the Write was in Claude's own signed plan**; `ls` held for approval. It even governed my other running Claude session.
5. **Close (15 s).** "Getting from sign-up to the first 'allowed' took about 6 workarounds. All of them are fixable, and I wrote each one down with a suggested fix (28 items in GAPS.md)."

## Gaps (I noticed… / How are you thinking about…? / I'd love to help with…)

1. **Tool-name rules vs. effects (GAPS #27, strongest).**
   - *I noticed* "deny Write and Edit" in ArmorClaude blocked the Edit tool, but a `cat >> file` through Bash still wrote the file, and the Bash "hold" didn't pause in auto mode.
   - *How are you thinking about* rules that follow what an action does (writes a file, opens the network) rather than the tool's name? Is that where the Intent Container comes in for coding agents?
   - *I'd love to help with* a small classifier for shell commands (read / write / delete / network) plus test cases for bypasses like this one.
2. **First-run experience (GAPS #9, #14, #15, #16, #18).**
   - *I noticed* the quickstart as written gives an HTTP 500 on a fresh account; the real reason was "no agent registered". Then: manual agent registration demands a URL, the SDK wants the agent's name not the UUID the console shows, and "no policy" means allow on the Gateway but block in the SDK.
   - *How are you thinking about* measuring time-to-first-allowed for new developers?
   - *I'd love to help with* a "fresh account" end-to-end test that runs the quickstart in CI and catches these regressions.
3. **Explainability of blocks (GAPS #25).**
   - *I noticed* the SDK and Gateway reasons are great (`allow:get_weather#0`, `tool-not-in-plan`), but ArmorClaude says `policy forbid: policy4`, an id neither I nor Claude could map to a rule.
   - *How are you thinking about* a consistent "why was this blocked" message across products, since explainability is the selling point?
   - *I'd love to help with* including the rule's human text in every verdict.
4. **One source of truth for policies (GAPS #20, #26).**
   - *I noticed* docs show `armor.io/v1` while the console makes `v2`; and an ArmorClaude rule confirmed in the terminal is only a proposal on the dashboard, so the next session can silently replace it.
   - *How are you thinking about* which side wins, terminal or dashboard?
   - *I'd love to help with* doc updates for the v2 format and a "your local rule was replaced" warning.

Praise to say early (be fair): the docs are agent-friendly (`llms.txt`, `/llms.mdx/<path>`), the Tools "Limits" page is honestly written, the installer is carefully engineered (no sudo, 0600 credentials, URL allow-list), and only a human can confirm an ArmorClaude policy.

## Contribution offers

1. **A one-line SDK fix, ready as a PR (GAPS #18).** `ArmorIQSession.declare_model_tools()` uses `self.client` where the attribute is `self._client`, so it crashes with `AttributeError`. That method is what fills the agent's tool list, which Policy Studio needs before it can activate a policy. Fix + a test.
2. **A prompt-injection test kit for coding agents.** Turn my playground (fake credentials, a note with a hidden instruction) into a repeatable scenario runner: each scenario tries a forbidden action by a different route (Write tool, Bash, a subprocess) and reports which ones ArmorIQ blocked. It catches bypasses like #27 and could seed a public benchmark.

## If asked "what would you do in your first week?"
Fix the first-run path (gaps #9–#16) with a CI test that signs up a fresh org and runs the quickstart, then start the injection test kit.
