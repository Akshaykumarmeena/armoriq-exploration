"""Check that the SDK imports and the API key in .env is present.

Never prints the key itself, only whether it's set and its length.
"""

import os

from dotenv import load_dotenv

load_dotenv()

import armoriq_sdk  # noqa: E402

print("armoriq_sdk imported, version:", getattr(armoriq_sdk, "__version__", "unknown"))

key = os.getenv("ARMORIQ_API_KEY", "")
if not key or key == "your-key-here":
    print("ARMORIQ_API_KEY: NOT SET (copy .env.example to .env and add your key)")
else:
    print(f"ARMORIQ_API_KEY: set ({len(key)} chars)")
    from armoriq_sdk import ArmorIQClient

    ArmorIQClient()
    print("ArmorIQClient() created OK")
