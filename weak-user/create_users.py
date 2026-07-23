# scripts/create_users.py

import grp
import json
import subprocess
import sys
from pathlib import Path


START_UID = 1111
TARGET_GID = 100


def run(command: list[str]) -> None:
    subprocess.run(command, check=True)


def ensure_gid_exists(gid: int) -> None:
    try:
        grp.getgrgid(gid)
    except KeyError:
        run(
            [
                "groupadd",
                "--gid",
                str(gid),
                "metasploitable-users",
            ]
        )


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit(
            "Usage: create_users.py <users.json>"
        )

    users = json.loads(
        Path(sys.argv[1]).read_text(encoding="utf-8")
    )

    ensure_gid_exists(TARGET_GID)

    uid = START_UID

    for account in users:
        username = account["username"]

        run(
            [
                "useradd",
                "--create-home",
                "--uid",
                str(uid),
                "--gid",
                str(TARGET_GID),
                "--shell",
                "/bin/bash",
                "--password",
                account["password_hash"],
                username,
            ]
        )

        if account["admin"]:
            run(
                [
                    "usermod",
                    "--append",
                    "--groups",
                    "sudo",
                    username,
                ]
            )

        uid += 1


if __name__ == "__main__":
    main()