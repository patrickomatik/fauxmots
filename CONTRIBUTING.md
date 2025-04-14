# Contributing to Fauxmots

Thank you for your interest in contributing to Fauxmots! This document provides guidelines and instructions for contributing.

## Development Setup

1. Fork the repository on GitHub.
2. Clone your fork locally:
   ```bash
   git clone https://github.com/YOUR-USERNAME/fauxmots.git
   cd fauxmots
   ```
3. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. For development, you may want to install additional dependencies:
   ```bash
   pip install pytest pytest-cov flake8
   ```

## Development Workflow

1. Create a new branch for your feature or bugfix:
   ```bash
   git checkout -b feature-branch-name
   ```
2. Make your changes.
3. Run tests to make sure everything works:
   ```bash
   python -m pytest
   ```
4. Lint your code:
   ```bash
   flake8
   ```
5. Commit your changes with a descriptive message.
6. Push your branch to GitHub:
   ```bash
   git push origin feature-branch-name
   ```
7. Create a Pull Request on GitHub.

## Coding Guidelines

- Follow PEP 8 style guide for Python code.
- Write docstrings for all modules, classes, and functions.
- Ensure tests are included for new features.
- Keep functions small and focused on a single responsibility.

## Testing

Run the test suite before submitting a PR:

```bash
python -m pytest
```

## Pull Request Process

1. Update the README.md if needed with details of changes.
2. Update the version number in any relevant files.
3. Your pull request will be reviewed by a maintainer.
4. Once approved, your PR will be merged.

## Code of Conduct

Please note that this project is released with a Contributor Code of Conduct. By participating in this project you agree to abide by its terms. Be respectful and considerate of others.

## Questions?

If you have any questions or need help, please open an issue on GitHub.
