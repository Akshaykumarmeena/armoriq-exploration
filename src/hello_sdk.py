"""Step 3: ArmorIQ SDK hello world.

The idea in one line: the agent writes down a plan, ArmorIQ signs it, and
any action that isn't in the signed plan is refused, even with a valid API key.

What it does:
  1. start_plan  -> ArmorIQ signs a one-step plan: "get the weather"
  2. check the planned tool    (get_weather) -> expected: allowed
  3. check an unplanned tool   (send_email)  -> expected: blocked, "tool-not-in-plan"

Uses the session API (client.for_user(email).start_session()), which asks
ArmorIQ for a decision without needing a real MCP server behind it.
The docs' invoke() quickstart needs a real "weather-mcp" and returned
HTTP 500 for us; see notes/GAPS.md.

Needs in .env: ARMORIQ_API_KEY, and ARMORIQ_AGENT_ID (an agent registered in
the console). Without an agent id, every call is blocked as "agent_unresolved".
"""

import os

from dotenv import load_dotenv

load_dotenv(".env")

from armoriq_sdk import ArmorIQClient  # noqa: E402

USER = os.getenv("DEMO_USER_EMAIL", "alice@example.com")
AGENT_ID = os.getenv("ARMORIQ_AGENT_ID")
if AGENT_ID in (None, "", "your-agent-id-here"):
    AGENT_ID = None

# Tool names are "<mcp>__<action>"; the session refuses bare names.
PLANNED = "weather-mcp__get_weather"
UNPLANNED = "weather-mcp__send_email"


def verdict(name, args, session):
    r = session.check(name, args)
    mark = "ALLOWED" if r.allowed else r.action.upper()
    print(f"  {name:28} -> {mark:7}  reason: {r.reason or '-'}")


def main():
    print(f"agent id: {AGENT_ID or 'NOT SET (expect agent_unresolved)'}")
    client = ArmorIQClient(agent_id=AGENT_ID)
    session = client.for_user(USER).start_session()

    token = session.start_plan(
        [{"name": PLANNED, "args": {"city": "San Francisco"}}],
        goal="Get weather for San Francisco",
    )
    pv = token.policy_validation or {}
    print(f"\n1. Plan signed: token {token.token_id}, plan_hash {token.plan_hash[:16]}...")
    print(f"   server policy check: validated={pv.get('validated')} reason={pv.get('reason')}")

    print("\n2-3. Ask ArmorIQ about each tool call:")
    verdict(PLANNED, {"city": "San Francisco"}, session)
    verdict(UNPLANNED, {"to": "attacker@evil.example", "body": "secrets"}, session)

    client.close()


if __name__ == "__main__":
    main()
