#!/usr/bin/env python3
"""qtop/PoH nonce verifier - PoC."""
import secrets
import subprocess
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("pip install pyyaml", file=sys.stderr)
    sys.exit(1)


def load_ledger(path):
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))


def generate_nonce():
    return secrets.token_hex(16)


def send_nonce(entry, nonce):
    print(f"  -> nonce for {entry['github']}: {nonce}")


def verify_signed_commit(commit_hash):
    try:
        result = subprocess.run(
            ["git", "verify-commit", commit_hash],
            capture_output=True, text=True, timeout=10
        )
        return result.returncode == 0
    except Exception:
        return False


def main():
    if len(sys.argv) < 2:
        print("Usage: python tools/poh_verify.py LEDGER_FILE", file=sys.stderr)
        return 2
    ledger = load_ledger(sys.argv[1])
    contributors = ledger.get("contributors", [])
    print(f"Loaded {len(contributors)} contributor(s)")
    for entry in contributors:
        nonce = generate_nonce()
        send_nonce(entry, nonce)
        commit = (entry.get("claims") or [{}])[0].get("signed_commit", "")
        verified = verify_signed_commit(commit) if commit else False
        status = "verified" if verified else "pending"
        print(f"  [{entry['github']}] {status}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
