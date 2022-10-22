# Lumos

cli tool that turns plain english into shell commands using openai's davinci-002 completion model.

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
