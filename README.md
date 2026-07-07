# Lumos

Lumos is a Python CLI that turns natural language into shell commands, explains existing commands, and keeps a local suggestion history.

I built it as a lightweight developer tool for moving from intent to shell command without leaving the terminal. It uses a small set of prompt examples, OpenAI completions, and a confirmation step before executing generated commands.

## Features

- Translate plain English into shell commands.
- Explain existing shell commands in plain English.
- Confirm before running generated commands.
- Run generated commands immediately with a flag.
- Store and display recent suggestions with execution history.

## Tech Stack

- Python
- Click
- Rich
- OpenAI
- python-dotenv

## Setup

```bash
pip install -e .
cp .env.example .env  # add your OpenAI API key
```

## Usage

```bash
lumos "find all python files larger than 1MB"
```

```
╭─ lumos ─────────────────────────────╮
│                                    │
│  $ find . -name "*.py" -size +1M   │
│                                    │
╰────────────────────────────────────╯

  run this command? [y/n]
```

Explain a command:

```bash
lumos -e "tar -xzf archive.tar.gz"
```

Run immediately without confirmation:

```bash
lumos -r "list files by size"
```

View suggestion history:

```bash
lumos -H
```

## Architecture

`lumos.cli` handles the terminal interface, command confirmation, execution, and history display. `lumos.engine` builds few-shot prompts for command generation and explanation, then calls the OpenAI completions API. `lumos.history` stores recent suggestions so users can review what was generated and whether it was executed.
