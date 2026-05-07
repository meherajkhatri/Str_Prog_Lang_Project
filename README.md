# Implementation of “for” Loop Syntactic Sugar

This project implements a complete interpreter for the **Trivial** programming language, enhanced with a structured `for` loop construct. The project demonstrates a standard compiler pipeline, including lexical analysis, recursive-descent parsing, and status-aware evaluation.

## Features
- **Expressions**: Arithmetic, comparison, and logical operators with correct precedence.
- **Statements**: Variable assignment, `print` statements, and block structures.
- **Control Flow**: `if/else`, `while` loops, and the newly added `for` loop.
- **Functions**: First-class functions with lexical scoping and parameter binding.
- **Status Handling**: Support for `return`, `break`, `continue`, and `exit` via status-aware evaluation.
- **Syntactic Sugar**: The `for` loop is implemented by desugaring it into a `while` loop at the parser level.

## Project Structure
- `tokenizer.py`: Uses Regular Expressions to convert source code into tokens
- `parser.py`: Implements a recursive-descent parser that generates an Abstract Syntax Tree (AST).
- `evaluator.py`: Traverses the AST and executes the program logic using environments.
- `runner.py`: The main entry point to execute `.t` source files.

## Installation & Usage(for Mac)
1. Ensure you have Python 3.x installed.
2. Place your source code in a file with a `.t` extension (e.g., `example.t`).
3. Run the interpreter using:
   ```bash
   python3 runner.py example.t