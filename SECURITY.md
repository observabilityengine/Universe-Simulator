# Security Policy

**Repository:** `observabilityengine/Universe-Simulator` (private)

## Scope

This repository is a private computational research kernel. It contains original implementations of algorithms, numerical methods, and infrastructure components. It is **not** a production service, network-facing application, or multi-user system.

## Supported Versions

| Version | Supported |
|---------|-----------|
| `main`  | Yes       |
| Other branches / tags | No |

Only the `main` branch receives updates.

## Security Considerations

### What this project is
- Collection of standalone, offline-executable Python modules
- Research and educational code
- No authentication service, no network listener by default, no persistent multi-user state

### What this project is not
- A web application or API server
- A cryptographic library intended for production secrets management
- A system that processes untrusted remote input by default

## Cryptographic & Security Modules

The following modules implement security-related primitives for research and demonstration purposes:

| Module | Purpose | Notes |
|--------|---------|-------|
| `security/password.py` | PBKDF2-HMAC-SHA256 password hashing | Suitable for study; use established libraries (e.g. Argon2, bcrypt) for production |
| `security/hmac_auth.py` | HMAC-SHA256 message authentication | Correct use of `hmac.compare_digest` |
| `crypto/merkle.py` | Merkle tree | Integrity proofs |
| `crypto/hashchain.py` | Append-only hash chain | Tamper-evident log |
| `crypto/otp.py` | One-time pad helpers | Educational only |

These implementations are original and intended for understanding and experimentation. They are **not** formally audited for production cryptographic use.

## Reporting a Vulnerability

If you discover a security-relevant issue in this repository (e.g. incorrect cryptographic construction, unsafe deserialization, or a logic flaw that could be dangerous if the code were reused in a privileged context):

1. **Do not** open a public GitHub issue.
2. Contact the repository owner directly via a private channel.
3. Provide a clear description of the issue, affected module(s), and (if possible) a minimal reproduction.

We will acknowledge receipt and assess the report. Because this is a private research repository with no external users or network exposure, there is no formal SLA or bug-bounty program.

## Safe Use Guidelines

- Treat all modules as **research code**.
- Do not use the cryptographic modules as the sole protection for real secrets or high-value systems without independent review.
- Be aware that `core/state.py` uses Python `pickle` for checkpoints — never unpickle data from untrusted sources.
- Modules that parse external formats (`protocol/http_parser.py`, etc.) are for controlled/demo input only.

## Dependencies

Runtime dependencies are limited and standard (NumPy, SciPy, SymPy, NetworkX where used). Keep the environment updated. No third-party web frameworks or authentication middleware are included.

## Policy Updates

This security policy may be updated on `main` as the project evolves. The version on the `main` branch is authoritative.
