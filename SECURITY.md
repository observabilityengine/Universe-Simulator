# Security Policy

**Repository:** [observabilityengine/Universe-Simulator](https://github.com/observabilityengine/Universe-Simulator)

## Scope

This repository is an **open-source computational research kernel**. It contains original implementations of algorithms, numerical methods, evolutionary computation, physics, finance, machine learning, and infrastructure components.

It is **not**:

- A production service
- A network-facing application or API server
- A multi-user system
- A cryptographic library intended for protecting real secrets in production

## Supported Versions

| Version               | Supported |
|-----------------------|-----------|
| `main`                | Yes       |
| Other branches / tags | No        |

Only the `main` branch receives updates and is considered supported.

## Security Considerations

### What this project is
- A collection of standalone, offline-executable Python modules
- Research and educational code released under the MIT License
- No authentication service, no default network listener, no persistent multi-user state

### What this project is not
- A web application or public API
- A production-grade cryptographic library
- A system designed to process untrusted remote input by default

## Cryptographic & Security Modules

The following modules implement security-related primitives for research and demonstration purposes only:

| Module / package        | Purpose                                      | Notes                                                                 |
|-------------------------|----------------------------------------------|-----------------------------------------------------------------------|
| `security/`             | Password hashing, HMAC helpers               | Prefer Argon2 / bcrypt for production                                 |
| `crypto/`               | Research hashes, Merkle trees, hash chains   | Educational / experimental                                            |
| `crypto_adv/`           | RSA, DH, ECC, ChaCha20, AES, HKDF, Poly1305  | Not formally audited                                                  |

These implementations are original and intended for understanding and experimentation. They have **not** been formally audited and must **not** be used as the sole protection for real secrets or high-value systems without independent expert review.

## Reporting a Vulnerability

If you discover a security-relevant issue (incorrect cryptographic construction, unsafe deserialization, logic flaw that could be dangerous if the code were reused in a privileged context, etc.):

1. **Prefer private disclosure** — open a [GitHub Security Advisory](https://github.com/observabilityengine/Universe-Simulator/security/advisories/new) if available, or contact the repository maintainers privately.
2. If private channels are unavailable, open a public issue with the label `security` and avoid including exploit details that could cause immediate harm.
3. Provide a clear description of the issue, the affected module(s), and (if possible) a minimal reproduction.

We will acknowledge reports and assess them as promptly as possible. There is currently no formal bug-bounty program.

## Safe Use Guidelines

- Treat **all** modules as research code.
- Do not use the cryptographic modules as the primary protection for real secrets without independent review.
- `core/state.py` uses Python `pickle` for checkpoints — **never** unpickle data from untrusted sources.
- Modules that parse external formats are intended for controlled / demo input only.
- Keep dependencies updated. Runtime dependencies are limited to standard scientific libraries (NumPy, SciPy, SymPy where used). No third-party web frameworks or authentication middleware are included.

## Dependencies

Runtime dependencies are intentionally minimal and standard. Keep the environment updated. No third-party web frameworks, authentication middleware, or network services are part of this repository.

## Policy Updates

This security policy may be updated on the `main` branch as the project evolves. The version present on `main` is authoritative.
