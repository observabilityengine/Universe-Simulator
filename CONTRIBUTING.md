# Contributing to Universe Simulator

Thanks for your interest in contributing.

## Quality bar

Every module must be:

- **Complete** — full end-to-end algorithm, no stubs or placeholders
- **Runnable** — works under `python -m package.module`
- **Self-testing** — `if __name__ == "__main__"` with real asserts (happy path + edge cases)
- **Original** — written for this repository; no copied proprietary code

See [README.md](README.md) and [TEST_SUITES.md](TEST_SUITES.md).

## Workflow

1. Fork the repository (or create a branch if you have write access).
2. Create a feature branch from `main`.
3. Make your changes. Add or update the module self-test.
4. Run the module:
   ```bash
   python -m package.module
   ```
5. Open a pull request against `main`.
6. Resolve review comments before merge.

`main` is protected: force pushes and direct commits are blocked; changes go through pull requests.

## Pull requests

- Keep PRs focused (one module or one coherent fix).
- Describe what changed and how you verified it.
- Do not add incomplete or non-runnable code.

## Security

Report security issues via [GitHub Security Advisories](https://github.com/observabilityengine/Universe-Simulator/security/advisories/new) when possible. See [SECURITY.md](SECURITY.md).

## License

By contributing, you agree that your contributions are licensed under the [MIT License](LICENSE).
