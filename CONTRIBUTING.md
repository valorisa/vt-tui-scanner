# Contributing to VT TUI Scanner

Thank you for considering contributing to VT TUI Scanner! This document provides guidelines and instructions for contributing.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Pull Request Process](#pull-request-process)
- [Coding Standards](#coding-standards)
- [Testing](#testing)

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Keep discussions professional

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/vt-tui-scanner.git`
3. Create a branch: `git checkout -b feature/your-feature`

## Development Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dev dependencies
pip install -r requirements.txt
pip install -e ".[dev]"

# Install pre-commit hooks (optional)
pre-commit install
```

## Pull Request Process

1. Ensure tests pass: `pytest tests/`
2. Run linting: `flake8 src/ tests/`
3. Update documentation if needed
4. Submit PR with clear description
5. Wait for review and address feedback

## Coding Standards

- **PEP 8** - Follow Python style guidelines
- **Type Hints** - Use typing for all function signatures
- **Docstrings** - Google style for all public functions
- **Line Length** - Maximum 100 characters
- **Imports** - Sorted and grouped (stdlib, third-party, local)

## Testing

```bash
# Run all tests
pytest tests/

# With coverage
pytest tests/ --cov=src --cov-report=html

# Specific test file
pytest tests/test_vt_client.py -v
```

## Questions?

Open an issue for any questions about contributing.
