# DARK8 OS - Contribution Guidelines

Thank you for your interest in contributing to DARK8 OS!

## How to Contribute

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/your-feature`
3. **Implement** your changes
4. **Add tests** for new functionality
5. **Run tests**: `make test`
6. **Format code**: `make format`
7. **Commit**: `git commit -am 'Add feature'`
8. **Push**: `git push origin feature/your-feature`
9. **Create** a Pull Request

## Development Setup

```bash
./scripts/setup_env.sh
make dev
```

## Code Style

- **Python**: PEP 8 with Black formatting
- **Naming**: snake_case for functions/variables, CamelCase for classes
- **Type hints**: Required for all functions
- **Docstrings**: Google style docstrings

## Testing

Add tests for all new features:

```bash
# Run all tests
make test

# Run specific test file
pytest tests/test_nlp.py -v

# With coverage
make test-cov
```

## Git Commit Messages

```
<type>: <subject>

<body>

<footer>
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `chore`

Example:
```
feat: Add Polish intent classifier

Implement BERT-based intent classification for Polish language.
Adds support for BUILD_APP, SEARCH, and GIT_OPERATION intents.

Closes #123
```

## Pull Request Guidelines

- Keep PRs focused on one feature
- Write clear PR description
- Link related issues
- Ensure all tests pass
- Update documentation

## Reporting Issues

- Use GitHub Issues
- Provide clear, reproducible steps
- Include error messages and logs
- Specify Python version and OS

## Questions?

- Open a GitHub Discussion
- Comment on related Issues
- Join our Discord (coming soon)

---

**Thank you for contributing to DARK8 OS! 🖤**
