# Repository Intelligence Analyzer

A Python-based static analysis tool that analyzes a Git repository, extracts Python code structure, tracks import dependencies, and performs automatic change-impact analysis.

## Features

- Analyzes Python files using Python AST
- Detects functions and classes
- Counts lines of code
- Extracts import dependencies between Python files
- Reads Git commit history using GitPython
- Identifies files changed in the latest commit
- Performs automatic change-impact analysis
- Reports potentially affected files
- Provides an analysis summary

## Tech Stack

- Python
- AST (Abstract Syntax Tree)
- GitPython
- Git

## Project Structure

```text
repository-intelligence-analyzer/
│
├── main.py
├── analyzer.py
├── utils.py
├── README.md
└── .gitignore