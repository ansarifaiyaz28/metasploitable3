# scripts/extract_users.py

import json
import re
import sys
from pathlib import Path


ENTRY_PATTERN = re.compile(
    r"default\[:users\]\[:(?P<key>[^\]]+)\]\s*=\s*"
    r"\{(?P<body>.*?)\}",
    re.DOTALL,
)


def get_string(body: str, field: str) -> str:
    match = re.search(
        rf"\b{re.escape(field)}:\s*'([^']*)'",
        body,
    )
    if not match:
        raise ValueError(f"Missing field: {field}")
    return match.group(1)


def get_boolean(body: str, field: str) -> bool:
    match = re.search(
        rf"\b{re.escape(field)}:\s*(true|false)",
        body,
    )
    if not match:
        raise ValueError(f"Missing field: {field}")
    return match.group(1) == "true"


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit(
            "Usage: extract_users.py "
            "<attributes/users.rb> <output.json>"
        )

    source = Path(sys.argv[1])
    output = Path(sys.argv[2])

    text = source.read_text(encoding="utf-8")

    users = []

    for entry in ENTRY_PATTERN.finditer(text):
        body = entry.group("body")

        users.append(
            {
                "username": get_string(body, "username"),
                "password_hash": get_string(body, "password_hash"),
                "first_name": get_string(body, "first_name"),
                "last_name": get_string(body, "last_name"),
                "admin": get_boolean(body, "admin"),
                "salary": get_string(body, "salary"),

            }
        )

    if not users:
        raise RuntimeError(
            "No users found. The upstream attributes format may have changed."
        )

    output.parent.mkdir(parents=True, exist_ok=True)

    output.write_text(
        json.dumps(users, indent=2) + "\n",
        encoding="utf-8",
    )

    print(f"Extracted {len(users)} users to {output}")


if __name__ == "__main__":
    main()