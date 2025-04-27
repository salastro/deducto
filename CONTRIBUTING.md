# Contributing to Deducto

Thank you for your interest in contributing to Deducto! We welcome contributions from everyone, and we’re excited to have you as part of the community. This document provides guidelines to help you get started.

## How to Contribute

### 1. Fork the Repository
To contribute, you’ll need to fork the repository. This creates a personal copy of the project where you can make your changes.

- Visit the [Deducto GitHub repository](https://github.com/salastro/deducto).
- Click on the **Fork** button in the top right corner.
- Clone your forked repository to your local machine:

  ```bash
  git clone https://github.com/YOUR-USERNAME/deducto.git
  cd deducto
  ```

### 2. Set Up Your Local Development Environment
Before you begin making changes, it’s important to set up the project locally. Deducto uses [Poetry](https://python-poetry.org/) for dependency management and building.

1. Install Poetry if you haven’t already:

   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

2. Install the project dependencies:

   ```bash
   poetry install
   ```

3. If you'd like to work in the project's virtual environment:

   ```bash
   poetry shell
   ```

### 3. Make Your Changes
Create a new branch for your changes:

```bash
git checkout -b feature-branch
```

Make your modifications, improvements, or bug fixes, and write tests if applicable.

### 4. Commit Your Changes
Once you’ve completed your changes, commit them with a descriptive message:

```bash
git add .
git commit -m "Add feature or fix bug"
```

### 5. Push Your Changes
Push your changes to your fork:

```bash
git push origin feature-branch
```

### 6. Create a Pull Request
Once you’ve pushed your changes, open a pull request to the `main` branch of the original repository. Provide a clear description of what changes you’ve made, why they are necessary, and any relevant context.

### 7. Code Review
After you submit your pull request, project maintainers will review your code. Be open to feedback and make any necessary changes to ensure your contribution meets the project’s standards.

### 8. Merge
Once your pull request has been approved, it will be merged into the main project.

## Code Style Guidelines

We strive for consistent code throughout the project. Please follow these guidelines:

- **Python code**: Use [PEP 8](https://peps.python.org/pep-0008/) as the primary style guide.
- **Commit messages**: Write clear, concise commit messages in the present tense. For example: "Fix bug in parsing logic" rather than "Fixed bug."
- **Tests**: If applicable, write tests to cover your changes. This ensures the software remains reliable.

## Reporting Bugs

If you find a bug or issue with the project, please file an issue on the [Issues](https://github.com/salastro/deducto/issues) page. Be sure to include the following details:

- A clear description of the bug.
- Steps to reproduce the bug.
- Expected vs. actual behavior.
- Any error messages or logs.
- The version of Deducto and your environment setup.

## License

By contributing to Deducto, you agree that your contributions will be licensed under the [GPL-3.0 License](LICENSE).

## Thank You!

We appreciate your time and effort in improving Deducto! If you have any questions or need help, feel free to reach out by creating an issue or contacting the project maintainers.

Happy coding! 👨‍💻👩‍💻
