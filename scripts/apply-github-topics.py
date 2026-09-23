#!/usr/bin/env python3
"""Merge approved GitHub topics into repositories.

Dry-run is the default. The script never accepts a token as a command-line
argument and never writes or prints the token. Set GITHUB_TOKEN only for
--apply after authenticating securely with a newly issued credential.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

API = "https://api.github.com"
ACCEPT = "application/vnd.github+json"
API_VERSION = "2022-11-28"


def request(url: str, *, token: str | None, method: str = "GET", data: bytes | None = None):
    headers = {
        "Accept": ACCEPT,
        "X-GitHub-Api-Version": API_VERSION,
        "User-Agent": "eks-containers-topic-organizer",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, headers=headers, method=method, data=data)
    with urllib.request.urlopen(req, timeout=30) as response:
        return json.load(response)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--owner", required=True, help="GitHub account or organization")
    parser.add_argument("--apply", action="store_true", help="Write merged topics to GitHub")
    parser.add_argument(
        "--map",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "github" / "repository-topics.json",
        help="Path to repository/topic JSON map",
    )
    args = parser.parse_args()

    token = os.environ.get("GITHUB_TOKEN") if args.apply else None
    if args.apply and not token:
        print("GITHUB_TOKEN must be set for --apply", file=sys.stderr)
        return 2

    topic_map = json.loads(args.map.read_text())
    failures = 0

    for repository, proposed in topic_map.items():
        url = f"{API}/repos/{args.owner}/{repository}/topics"
        try:
            result = request(url, token=token)
            existing = result.get("names", [])
            merged = sorted(set(existing) | set(proposed))
            additions = sorted(set(merged) - set(existing))

            if len(merged) > 20:
                print(f"ERROR {repository}: merged topic count {len(merged)} exceeds GitHub limit")
                failures += 1
                continue

            print(f"{repository}")
            print(f"  existing: {', '.join(existing) or '(none)'}")
            print(f"  add:      {', '.join(additions) or '(none)'}")
            print(f"  final:    {', '.join(merged)}")

            if args.apply and additions:
                payload = json.dumps({"names": merged}).encode()
                request(url, token=token, method="PUT", data=payload)
                print("  result:   updated")
            else:
                print("  result:   dry-run" if not args.apply else "  result:   unchanged")
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError) as exc:
            print(f"ERROR {repository}: {exc}", file=sys.stderr)
            failures += 1

    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
