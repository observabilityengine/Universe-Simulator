# Security Policy

**Repository:** `observabilityengine/Universe-Simulator` (private)

## Scope

This repository is a **private computational research kernel**. It contains original implementations of algorithms, numerical methods, evolutionary computation, physics, finance, machine learning, and infrastructure components.

It is **not**:

- A production service
- A network-facing application or API server
- A multi-user system
- A cryptographic library intended for protecting real secrets in production

## Supported Versions

| Version              | Supported |
|----------------------|-----------|
| `main`               | Yes       |
| Other branches / tags| No        |

Only the `main` branch receives updates and is considered supported.

## Security Considerations

### What this project is
- A collection of standalone, offline-executable Python modules
- Research and educational code
- No authentication service, no default network listener, no persistent multi-user state

### What this project is not
- A web application or public API
- A production-grade cryptographic library
- A system designed to process untrusted remote input by default

## Cryptographic & Security Modules

The following modules implement security-related primitives for research and demonstration purposes only:

| Module                  | Purpose                              | Notes                                                                 |
|-------------------------|--------------------------------------|-----------------------------------------------------------------------|
| `security/password.py`  | PBKDF2-HMAC-SHA256 password hashing  | Suitable for study; prefer Argon2 / bcrypt for production             |
| `security/hmac_auth.py` | HMAC-SHA256 message authentication   | Uses `hmac.compare_digest` correctly                                  |
| `crypto/merkle.py`      | Merkle tree                          | Integrity proofs                                                      |
| `crypto/hashchain.py`   | Append-only hash chain               | Tamper-evident log                                                    |
| `crypto/otp.py`         | One-time pad helpers                 | Educational only                                                      |

These implementations are original and intended for understanding and experimentation. They have **not** been formally audited and must **not** be used as the sole protection for real secrets or high-value systems without independent expert review.

## Reporting a Vulnerability

If you discover a security-relevant issue (incorrect cryptographic construction, unsafe deserialization, logic flaw that could be dangerous if the code were reused in a privileged context, etc.):

1. **Do not** open a public GitHub issue.
2. Contact the repository owner directly via a private channel.
3. Provide a clear description of the issue, the affected module(s), and (if possible) a minimal reproduction.

Reports will be acknowledged and assessed. Because this is a private research repository with no external users or network exposure, there is no formal SLA or bug-bounty program.

## Safe Use Guidelines

- Treat **all** modules as research code.
- Do not use the cryptographic modules as the primary protection for real secrets without independent review.
- `core/state.py` uses Python `pickle` for checkpoints — **never** unpickle data from untrusted sources.
- Modules that parse external formats (e.g. `protocol/http_parser.py`) are intended for controlled / demo input only.
- Keep dependencies updated. Runtime dependencies are limited to standard scientific libraries (NumPy, SciPy, SymPy, NetworkX where used). No third-party web frameworks or authentication middleware are included.

## Dependencies

Runtime dependencies are intentionally minimal and standard. Keep the environment updated. No third-party web frameworks, authentication middleware, or network services are part of this repository.

## Policy Updates

This security policy may be updated on the `main` branch as the project evolves. The version present on `main` is authoritative.
