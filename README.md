# Deducto

Deducto is an interactive proof assistant built to assist in logical reasoning. It provides a REPL interface for users to input premises, set goals, and apply logical rules to derive conclusions. It offers a dynamic environment for users to step through logical reasoning using custom rules and operators, supporting undo, delete, and reset functionality.

## Features

- **Interactive REPL**: Allows users to input variables, premises, and goals interactively.
- **Rule-based Inference**: Users can apply logical rules to derive conclusions from premises.
- **Undo & Reset**: Track steps and backtrack when necessary.
- **Customizable Operators**: Define logical expressions using standard logical operators (AND, OR, IMPLIES, etc.).
- **Step-through Logic**: Users can view and manipulate each proof step.

## Installation

The recommended way to install Deducto is through [Poetry](https://python-poetry.org/), which handles dependencies and builds efficiently.

### Prerequisites

Ensure you have Python 3.7 or higher installed. Then, install Poetry by following the [Poetry installation instructions](https://python-poetry.org/docs/#installation).

### Steps to Install

1. Clone the repository:

   ```bash
   git clone https://github.com/salastro/deducto.git
   cd deducto
   ```

2. Install dependencies and build the project:

   ```bash
   poetry install
   ```

3. If you'd like to work on the project locally, you can activate the virtual environment:

   ```bash
   poetry shell
   ```

## Usage

After installation, you can run the program by executing the following command:

```bash
poetry run deducto
```

This will start the interactive REPL, where you can:

- Input variables (e.g., `a, b, c`).
- Define premises (e.g., `a -> b, b -> c`).
- Set a goal (e.g., `a -> c`).
- Apply logical rules to reach conclusions.
- Use commands like `undo`, `delete <step_number>`, `reset`, and `exit`.

### Example

```
Variables: a, b, c
Premises:
  1. a → b
  2. b → c
Goal: a → c
Apply: hypothetical_syllogism 1 2
✓ Goal reached!

Proof Steps:
1. a → b    (assumption)
2. b → c    (assumption)
3. a → c    (hypothetical_syllogism from 1, 2)
```

## Commands

- **[rule targets]**: Apply a logical rule to the specified targets. Rules include inference and equivalence rules.
- **undo**: Undo the last step.
- **delete <n>**: Delete the step corresponding to index `n`.
- **reset**: Reset to the original assumptions (premises).
- **exit**: Exit the program.

## Contributing

If you'd like to contribute to the project, feel free to fork the repository and submit a pull request with your changes.

For more detailed information on contributing, check the [Contributing guidelines](CONTRIBUTING.md).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
