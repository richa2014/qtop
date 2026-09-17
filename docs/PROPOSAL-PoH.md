# Proposal: Lighter, More Rewarding, More Engaging PoH

**Issue:** qtop/qtop#551  
**Author:** @richa2014

## Problem

Current contributors face friction:
- ssh-keygen -Y sign requires setup most casual contributors lack
- Unsigned PRs from bots pollute the queue
- Keybase/Keyoxide are powerful but add steps

We need verification that is:
1. Low-friction - one command
2. Sybil-resistant - bots cannot fake identity
3. Multi-source - not tied to one provider
4. Rewarding - gamified

## Proposed Design: qtop/PoH sub-repo

A dedicated repo (qtop/PoH) with a single YAML ledger.

### Ledger Format

See docs/poh_example.yaml

### Verification Flow

1. Contributor opens PR to qtop/PoH with signed commit
2. CI bot parses YAML, sends nonce to email
3. Contributor replies with nonce signed by same key
4. Bot verifies signature
5. If verified, PR auto-merges

### Anti-Bot Rules

- Identities must be resolvable (Keybase, Keyoxide, LinkedIn)
- Nonce signed by same key as commit
- Max 5 claims per person
- Duplicate emails rejected

## Proof of Concept

Two files in this PR:
1. docs/poh_example.yaml - example ledger
2. tools/poh_verify.py - working verifier

Run: python tools/poh_verify.py docs/poh_example.yaml

## Why This Is Better

| Approach | Setup | Sybil-Resistant | Multi-Source |
|---|---|---|---|
| ssh-keygen -Y sign | High | Yes | No |
| Keybase only | Medium | Yes | No |
| qtop/PoH (this) | Low | Yes | Yes |

## Next Steps

If accepted I can build the CI bot, validator, and docs.