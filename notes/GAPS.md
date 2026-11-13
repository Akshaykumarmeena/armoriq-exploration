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
