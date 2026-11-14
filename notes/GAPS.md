# Gaps and friction

Format for each item: **Where** · **Expected** · **What happened** · **Suggested fix** · **Severity** (low / medium / high).

## SDK docs vs SDK 0.8.18

### 1. `invoke()` Python signature in docs doesn't match the package
- **Where:** `/sdk/core-methods/invoke` (Python tab)
- **Expected:** the documented signature `invoke(mcp, action, intent_token, params=None, merkle_proof=None, user_email=None)` and the example `client.invoke(..., timeout=120)` to work.
- **What happened:** the installed signature is `invoke(mcp, action, intent_token, params=None, user_email=None)`. There is no `merkle_proof` and no `timeout`. So the documented `timeout=120` example would raise `TypeError`, and anyone passing `user_email` positionally per the docs' order would put it in the wrong slot. (Checked with `inspect.signature`, not yet by running the call.)
- **Suggested fix:** regenerate the Python reference from the code (e.g. from docstrings/signatures in CI), drop `timeout` from the example or add it to the SDK.
- **Severity:** medium (copy-paste breaks)

### 2. `invoke()` return shape differs between tabs and within the page
- **Where:** `/sdk/core-methods/invoke`
- **Expected:** one result shape.
- **What happened:** Python shows a dict (`result["success"]`, `execution_time_ms` in ms); TypeScript shows `MCPInvocationResult` with `result`, `status`, `verified`, `executionTime` in **seconds**. The Python error-handling example uses `client.get_intent_token(plan)["token"]`, while the overview page uses the return value directly as the token.
- **Suggested fix:** align units and access style; one canonical example per language that is tested.
- **Severity:** low–medium

### 3. `delegate()` Python signature omits `target_agent`
- **Where:** `/sdk/core-methods/delegate`
- **What happened:** the TypeScript signature has `targetAgent`; the Python one in the docs doesn't, but the real Python method does (`target_agent: Optional[str] = None`). The Python example also reads `delegation_result.delegation_id` (attribute) while "Returns" shows a dict.
- **Suggested fix:** add `target_agent` to the Python table; pick attribute or dict access.
- **Severity:** low

### 4. `reanchor()` / `refine()` / `delegate_subtree()` are barely documented
- **Where:** SDK reference
- **What happened:** `reanchor` appears 3 times in the full docs, `refine(` and `delegate_subtree` 0 times, `armoriq policy` (CLI) 0 times. These look like the answer to "how do re-planning agents work?", which is one of the most interesting questions for the product.
- **Suggested fix:** a "Re-planning and long-running agents" guide: when to re-mint, when to `reanchor`, what triggers a hold. Note that tokens default to a 60-second validity.
- **Severity:** medium (strategic)

## Docs consistency

### 5. Gateway rate limit: 120/min or 600/min?
- **Where:** `/products/intent-gateway` ("about 120 policy calls a minute") vs `/products/intent-gateway/monitor-mode` ("up to 600 requests per minute per gateway key").
- **Expected:** one number, or an explanation that monitor and enforce modes differ.
- **Suggested fix:** state both limits in one table with what happens past each (enforce: withheld; monitor: runs unchecked).
- **Severity:** low

### 6. CLI command lists differ across pages
- **Where:** `/sdk` lists `… orgs, keys, status, logs`; `/sdk/installation` lists `… logout, whoami, orgs, switch-org, status, logs` (no `keys`). The real 0.8.18 CLI has both sets **plus `policy`**.
- **Suggested fix:** generate the list from `armoriq --help`.
- **Severity:** low

## Onboarding

### 7. Two consoles, two sign-ups
- **Where:** platform.armoriq.ai (SDK, Gateway, policies) vs tools.armoriq.ai (ArmorClaude/ArmorCodex).
- **Expected:** one ArmorIQ account.
- **What happened:** Tools quickstart says "You need an account at tools.armoriq.ai" and describes its own sign-up. To verify in step 6 whether the platform account carries over.
- **Suggested fix:** a short "which console do I use?" note on the docs home, or SSO between them.
- **Severity:** medium (first-run confusion)

### 8. Small doc nits
- `/sdk/installation` repeats "See Integrations…" twice at the end.
- Markdown escaping in the `/llms.mdx/` export: `**API Keys → Create*&#x2A;` on the Create API Key page and similar on Policies and Tools Limits. Affects AI agents reading the docs; not yet checked whether the rendered site shows it.
- **Severity:** low

## Step 3 hands-on (SDK hello world)

### 9. Quickstart doesn't work on a fresh account: HTTP 500 from the proxy
- **Where:** `/platform/sdk-cli/quickstart` ("That's it.") and the `/sdk` overview example.
- **Expected:** with a valid API key, the example's planned call succeeds and the unplanned call raises a clear "not in plan" error.
- **What happened:** the token was minted fine, but both `invoke` calls returned `MCPInvocationException ... (HTTP 500): Internal Proxy Error`. Allowed and blocked calls were indistinguishable. Likely causes: no agent registered and no real `weather-mcp` behind the proxy.
- **Suggested fix:** (a) return a 4xx with the real reason (`agent_unresolved`, `mcp_not_found`) instead of 500; (b) host a public demo MCP (e.g. `demo-weather-mcp`) so the quickstart runs end to end; (c) add "register an agent first" as step 0.
- **Severity:** high (first five minutes of every new developer)

### 10. "No agent IDs to manage" vs `agent_unresolved`
- **Where:** `/sdk` ("no user/agent IDs to manage") and `/sdk/client-initialization` ("remove `user_id` / `agent_id`… resolved per-request").
- **What happened:** with only an API key, every decision is `block` with `agent_unresolved: pass agent_id (or set AGENT_ID) to decide calls in local mode`. The `ArmorIQClient(agent_id=...)` parameter exists in 0.8.18 but isn't in the documented parameter table.
- **Suggested fix:** document when an agent id is needed, add `agent_id` to the parameter table, and link "Add Agent" from the SDK quickstart.
- **Severity:** high

### 11. Session API needs `<mcp>__<action>` tool names; not in the docs example
- **Where:** `/sdk/client-initialization` "Per-user scopes" example uses `{"action": "fetch_sales", "mcp": "data-mcp"}` and `session.check("fetch_sales", …)`.
- **What happened:** with real 0.8.18, `start_plan` raised `ValueError: Tool "get_weather" is not namespaced as <MCP>__<action> and no default_mcp_name was set on the session.`
- **Suggested fix:** show the `mcp__action` convention (or `default_mcp_name`) in the example.
- **Severity:** medium

### 12. Token lifetime: docs say 5 minutes, SDK default is 60 seconds
- **Where:** quickstart comment "Get a short-lived intent token (5 minutes by default)" while passing `validity_seconds=300`; `get_intent_token` signature default is `validity_seconds=60.0`.
- **Suggested fix:** correct the comment.
- **Severity:** low

### 13. Two parallel SDK doc trees
- `/sdk/...` and `/platform/sdk-cli/...` both document the SDK, with different examples (e.g. the TS quickstart still passes `userId`/`agentId`, which the other tree says to remove).
- **Suggested fix:** pick one tree and redirect the other.
- **Severity:** low–medium

### 14. Manual agent registration fails: "url should not be empty" (bug)
- **Where:** platform.armoriq.ai → Inventory → Agents → Add AI agent, Method = Manual.
- **Expected:** the wizard's own text says manual registration needs no URL. Step "Connect" shows "You can add a URL later from the agent detail page" and makes you tick "I understand this agent has no URL". So Register should succeed.
- **What happened (2026-11-13):** on the Review step, **Register agent** fails with `url must be a URL address. url should not be empty`. The frontend allows an empty URL, the backend validation rejects it. Screenshots taken. Also: the docs page `/platform/agents/add-agent` describes an older wizard (URL field in Agent Details), and the breadcrumb says "Step 4 of 4" while the stepper shows 5 steps.
- **Suggested fix:** make `url` optional in the backend DTO for manual agents (or send `null` instead of `""`), and add a test for the manual path; refresh the docs screenshots.
- **Severity:** high: an SDK-only developer can't register an agent, and without an agent every SDK call is `agent_unresolved`. Steps 9, 10 and 14 together block the whole SDK hello world on a fresh account.

### 15. SDK `agent_id` wants the agent **name**, not the ID the console shows
- **Where:** SDK `ArmorIQClient(agent_id=...)` / `AGENT_ID`; console agent detail page.
- **What happened:** with the UUID copied from the console (`1e849d07-…`), every call returned `agent_unresolved: no registered agent matches '1e849d07-…'`. With the agent's name `hello-weather-agent` it resolved (next error became `no_active_policy`).
- **Suggested fix:** accept either; or label the right value in the console ("SDK agent id: hello-weather-agent") with a copy button; document it next to the parameter.
- **Severity:** medium

### 16. "No active policy" means allow on the Gateway but block in the SDK
- **Where:** `/products/intent-gateway/enforcement`: "An agent with no active policy has its tool calls allowed, and each one is recorded." The Add Agent wizard also says "Calls are logged but unrestricted" when skipping policy.
- **What happened:** in the SDK, a registered agent with no policy blocks even the planned call: `reason: no_active_policy`.
- **Suggested fix:** make the behaviour consistent, or state clearly that the SDK defaults to deny, and have the wizard's text say so.
- **Severity:** medium (the wizard text is misleading)

### 17. `armoriq policy show` needs `armoriq login` even when `ARMORIQ_API_KEY` is set
- `Error: Not logged in (no active profile in ~/.armoriq/credentials.json)`. The SDK accepts the env key; the CLI doesn't. Minor, but surprising.
- **Severity:** low

### 18. SDK bug: `session.declare_model_tools()` crashes
- **Where:** `armoriq_sdk/session.py` line ~1099 (0.8.18).
- **What happened:** `AttributeError: 'ArmorIQSession' object has no attribute 'client'. Did you mean: '_client'?` The method uses `self.client`, the attribute is `self._client`.
- **Suggested fix:** one-character fix (`self._client`) plus a unit test that calls it.
- **Severity:** medium (easy fix, good first contribution)

### 19. Tool inventory push rejected: `POST /iap/sdk/tools` → 400 `invalid_body`
- **What happened:** calling the lower-level `integrations.openai.declare_model_tools(client, tools)` with standard OpenAI tool definitions logged `tool snapshot rejected (400) for hello-weather-agent: invalid_body`. The failure is only visible with DEBUG logging; by design "inventory problems never stop an agent".
- **Effect:** the agent shows "No tools yet" in Policy Studio, and Policy Studio refuses to activate a policy with "At least one governed tool is required". So an SDK-only agent can't get a policy through the form.
- **Suggested fix:** fix the payload; surface a WARNING-level hint when the push fails; let Policy Studio add a tool by name.
- **Severity:** high (chained with #14–#16, blocks the hello world)

### 20. Policy formats: docs show `armor.io/v1` (`memberRules`, `allowedTools`), console generates `armor.io/v2` (`spec.tools.default`, `rules`)
- No public reference for the v2 `rules` syntax that I could find in `llms-full.txt`.
- **Suggested fix:** a policy format reference page for v2 with an allow/block example.
- **Severity:** medium (also listed as a known gap in my research)
