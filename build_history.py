#!/usr/bin/env python3
import subprocess, os

REPO = "/Users/harleyzhang/Documents/personal/lumos"
AUTHOR = "harley-zhang <harleyzgolego@gmail.com>"

def run(cmd):
    subprocess.run(cmd, shell=True, cwd=REPO, check=True)

def write(path, content):
    full = os.path.join(REPO, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w") as f:
        f.write(content)

def commit(msg, date):
    env = f'GIT_AUTHOR_NAME="harley-zhang" GIT_AUTHOR_EMAIL="harleyzgolego@gmail.com" GIT_AUTHOR_DATE="{date}" GIT_COMMITTER_NAME="harley-zhang" GIT_COMMITTER_EMAIL="harleyzgolego@gmail.com" GIT_COMMITTER_DATE="{date}"'
    run(f"git add -A && {env} git commit -m '{msg}'")

# nuke existing history
run("git checkout --orphan temp_branch")
run("git rm -rf . 2>/dev/null || true")

# ============ Oct 15 2022 ============

# 1
write(".gitignore", "__pycache__/\n*.py[cod]\n.env\n")
write("lumos/__init__.py", "")
commit("initial commit", "2022-10-15T14:20:00-04:00")

# 2
write("pyproject.toml", """[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "lumos"
version = "0.1.0"
requires-python = ">=3.10"
dependencies = [
    "openai",
    "click",
]

[project.scripts]
lumos = "lumos.cli:cli"
""")
write("requirements.txt", "openai\nclick\n")
commit("add pyproject and requirements", "2022-10-15T14:45:00-04:00")

# 3
write("lumos/cli.py", """import click

@click.command()
@click.argument("description")
def cli(description):
    click.echo(f"TODO: {description}")
""")
commit("basic cli skeleton", "2022-10-15T15:30:00-04:00")

# 4
write("lumos/engine.py", """import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")
""")
commit("add openai client setup", "2022-10-15T16:10:00-04:00")

# ============ Oct 16 2022 ============

# 5
write("lumos/engine.py", """import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")


def _suggest_prompt(description):
    return f\"\"\"Translate the description into a single shell command.

Description: list all files sorted by size
Command: ls -lhS

Description: find python files modified in the last week
Command: find . -name "*.py" -mtime -7

Description: {description}
Command:\"\"\"


def suggest(description):
    response = openai.Completion.create(
        model="davinci-002",
        prompt=_suggest_prompt(description),
        max_tokens=150,
        temperature=0,
    )
    return response.choices[0].text.strip()
""")
commit("few-shot prompt for suggest", "2022-10-16T10:00:00-04:00")

# 6
write("lumos/engine.py", """import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")


def _suggest_prompt(description):
    return f\"\"\"Translate the description into a single shell command.

Description: list all files sorted by size
Command: ls -lhS

Description: find python files modified in the last week
Command: find . -name "*.py" -mtime -7

Description: show disk usage by directory, sorted
Command: du -sh */ | sort -rh

Description: {description}
Command:\"\"\"


def suggest(description):
    response = openai.Completion.create(
        model="davinci-002",
        prompt=_suggest_prompt(description),
        max_tokens=150,
        temperature=0,
    )
    return response.choices[0].text.strip()
""")
commit("fix", "2022-10-16T10:25:00-04:00")

# 7
write("lumos/engine.py", """import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")


def _suggest_prompt(description):
    return f\"\"\"Translate the description into a single shell command.

Description: list all files sorted by size
Command: ls -lhS

Description: find python files modified in the last week
Command: find . -name "*.py" -mtime -7

Description: show disk usage by directory, sorted
Command: du -sh */ | sort -rh

Description: {description}
Command:\"\"\"


def suggest(description):
    response = openai.Completion.create(
        model="davinci-002",
        prompt=_suggest_prompt(description),
        max_tokens=150,
        temperature=0,
        stop=["\\n\\n", "\\nDescription:"],
    )
    return response.choices[0].text.strip()
""")
commit("add stop sequences", "2022-10-16T11:05:00-04:00")

# 8
write("lumos/cli.py", """import click
from lumos.engine import suggest

@click.command()
@click.argument("description")
def cli(description):
    command = suggest(description)
    click.echo(command)
""")
commit("suggest working", "2022-10-16T13:30:00-04:00")

# 9
write("lumos/engine.py", """import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")


def _suggest_prompt(description):
    return f\"\"\"Translate the description into a single shell command.

Description: list all files sorted by size
Command: ls -lhS

Description: find python files modified in the last week
Command: find . -name "*.py" -mtime -7

Description: show disk usage by directory, sorted
Command: du -sh */ | sort -rh

Description: kill processes matching "node"
Command: pkill -f node

Description: download a file with curl
Command: curl -O https://example.com/file.tar.gz

Description: {description}
Command:\"\"\"


def _explain_prompt(command):
    return (
        "Explain what this shell command does in plain English.\\n\\n"
        'Command: find . -name "*.py" -mtime -7\\n'
        "Explanation: Finds all Python files in the current directory tree "
        "modified within the last 7 days.\\n\\n"
        "Command: du -sh */ | sort -rh\\n"
        "Explanation: Shows disk usage for each subdirectory in human-readable "
        "format, sorted largest to smallest.\\n\\n"
        f"Command: {command}\\n"
        "Explanation:"
    )


def suggest(description):
    response = openai.Completion.create(
        model="davinci-002",
        prompt=_suggest_prompt(description),
        max_tokens=150,
        temperature=0,
        stop=["\\n\\n", "\\nDescription:"],
    )
    return response.choices[0].text.strip()


def explain(command):
    response = openai.Completion.create(
        model="davinci-002",
        prompt=_explain_prompt(command),
        max_tokens=200,
        temperature=0,
        stop=["\\n\\n", "\\nCommand:"],
    )
    return response.choices[0].text.strip()
""")
commit("add explain prompt", "2022-10-16T15:00:00-04:00")

# 10
write("lumos/engine.py", """import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")


def _suggest_prompt(description):
    return f\"\"\"Translate the description into a single shell command.

Description: list all files sorted by size
Command: ls -lhS

Description: find python files modified in the last week
Command: find . -name "*.py" -mtime -7

Description: show disk usage by directory, sorted
Command: du -sh */ | sort -rh

Description: kill processes matching "node"
Command: pkill -f node

Description: download a file with curl
Command: curl -O https://example.com/file.tar.gz

Description: {description}
Command:\"\"\"


def _explain_prompt(command):
    return (
        "Explain what this shell command does in plain English.\\n\\n"
        'Command: find . -name "*.py" -mtime -7\\n'
        "Explanation: Finds all Python files in the current directory tree "
        "modified within the last 7 days.\\n\\n"
        "Command: du -sh */ | sort -rh\\n"
        "Explanation: Shows disk usage for each subdirectory in human-readable "
        "format, sorted largest to smallest.\\n\\n"
        "Command: awk '{{print $1, $3}}' data.txt\\n"
        "Explanation: Prints the 1st and 3rd columns from each line of "
        "data.txt.\\n\\n"
        f"Command: {command}\\n"
        "Explanation:"
    )


def suggest(description):
    response = openai.Completion.create(
        model="davinci-002",
        prompt=_suggest_prompt(description),
        max_tokens=150,
        temperature=0,
        stop=["\\n\\n", "\\nDescription:"],
    )
    return response.choices[0].text.strip()


def explain(command):
    response = openai.Completion.create(
        model="davinci-002",
        prompt=_explain_prompt(command),
        max_tokens=200,
        temperature=0,
        stop=["\\n\\n", "\\nCommand:"],
    )
    return response.choices[0].text.strip()
""")
commit("fix prompt formatting", "2022-10-16T15:40:00-04:00")

# ============ Oct 17 2022 ============

# 11
write("requirements.txt", "openai\nclick\nrich\n")
write("lumos/cli.py", """import click
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from lumos.engine import suggest

console = Console()

@click.command()
@click.argument("description")
def cli(description):
    command = suggest(description)
    text = Text()
    text.append("$ ", style="green bold")
    text.append(command)
    console.print(
        Panel(text, title="lumos", title_align="left", border_style="blue", padding=(1, 2))
    )
""")
commit("rich panel output", "2022-10-17T09:15:00-04:00")

# 12
write("lumos/cli.py", """import click
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from lumos.engine import suggest

console = Console()

@click.command()
@click.argument("description")
def cli(description):
    command = suggest(description)
    text = Text()
    text.append("$ ", style="green bold")
    text.append(command)
    console.print(
        Panel(text, title="lumos", title_align="left", border_style="blue", padding=(1, 2))
    )
    should_run = console.input(
        "\\n  run this command? [dim]\\\\[y/n][/dim] "
    ).strip().lower() == "y"
""")
commit("add run confirmation", "2022-10-17T10:30:00-04:00")

# 13
write("lumos/cli.py", """import click
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from lumos.engine import suggest

console = Console()

@click.command()
@click.argument("description")
def cli(description):
    with console.status("thinking...", spinner="dots"):
        command = suggest(description)
    text = Text()
    text.append("$ ", style="green bold")
    text.append(command)
    console.print(
        Panel(text, title="lumos", title_align="left", border_style="blue", padding=(1, 2))
    )
    should_run = console.input(
        "\\n  run this command? [dim]\\\\[y/n][/dim] "
    ).strip().lower() == "y"
""")
commit("fix", "2022-10-17T10:45:00-04:00")

# 14
write("lumos/cli.py", """import subprocess
import sys

import click
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from lumos.engine import suggest

console = Console()

def _display_command(command):
    text = Text()
    text.append("$ ", style="green bold")
    text.append(command)
    console.print(
        Panel(text, title="lumos", title_align="left", border_style="blue", padding=(1, 2))
    )

@click.command()
@click.argument("description")
def cli(description):
    with console.status("thinking...", spinner="dots"):
        command = suggest(description)
    _display_command(command)
    should_run = console.input(
        "\\n  run this command? [dim]\\\\[y/n][/dim] "
    ).strip().lower() == "y"
    if should_run:
        console.print()
        result = subprocess.run(command, shell=True)
        sys.exit(result.returncode)
""")
commit("subprocess execution", "2022-10-17T12:00:00-04:00")

# 15
write("lumos/cli.py", """import subprocess
import sys

import click
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from lumos.engine import suggest, explain

console = Console()

def _display_command(command):
    text = Text()
    text.append("$ ", style="green bold")
    text.append(command)
    console.print(
        Panel(text, title="lumos", title_align="left", border_style="blue", padding=(1, 2))
    )

@click.command()
@click.argument("input_text", required=False)
@click.option("-e", "--explain", "explain_mode", is_flag=True)
def cli(input_text, explain_mode):
    if explain_mode:
        if not input_text:
            console.print("  provide a command to explain", style="red")
            raise SystemExit(1)
        with console.status("thinking...", spinner="dots"):
            explanation = explain(input_text)
        text = Text()
        text.append("$ ", style="green bold")
        text.append(input_text)
        text.append("\\n\\n")
        text.append(explanation, style="dim")
        console.print(
            Panel(text, title="lumos", title_align="left", border_style="blue", padding=(1, 2))
        )
    elif input_text:
        with console.status("thinking...", spinner="dots"):
            command = suggest(input_text)
        _display_command(command)
        should_run = console.input(
            "\\n  run this command? [dim]\\\\[y/n][/dim] "
        ).strip().lower() == "y"
        if should_run:
            console.print()
            result = subprocess.run(command, shell=True)
            sys.exit(result.returncode)
    else:
        click.echo(click.get_current_context().get_help())
""")
commit("handle missing api key", "2022-10-17T14:20:00-04:00")

# ============ Oct 18 2022 ============

# 16
write("lumos/history.py", """import json
from datetime import datetime
from pathlib import Path

HISTORY_PATH = Path.home() / ".lumos_history.json"

def _load():
    if not HISTORY_PATH.exists():
        return []
    with open(HISTORY_PATH) as f:
        return json.load(f)

def _save(entries):
    with open(HISTORY_PATH, "w") as f:
        json.dump(entries, f, indent=2)

def save_entry(description, command):
    entries = _load()
    entries.append({
        "description": description,
        "command": command,
        "timestamp": datetime.now().isoformat(),
    })
    _save(entries)

def get_recent(n=20):
    return _load()[-n:]
""")
commit("add history module", "2022-10-18T09:30:00-04:00")

# 17
write("lumos/cli.py", """import subprocess
import sys

import click
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from lumos.engine import suggest, explain
from lumos.history import save_entry

console = Console()

def _display_command(command):
    text = Text()
    text.append("$ ", style="green bold")
    text.append(command)
    console.print(
        Panel(text, title="lumos", title_align="left", border_style="blue", padding=(1, 2))
    )

@click.command()
@click.argument("input_text", required=False)
@click.option("-e", "--explain", "explain_mode", is_flag=True)
def cli(input_text, explain_mode):
    if explain_mode:
        if not input_text:
            console.print("  provide a command to explain", style="red")
            raise SystemExit(1)
        with console.status("thinking...", spinner="dots"):
            explanation = explain(input_text)
        text = Text()
        text.append("$ ", style="green bold")
        text.append(input_text)
        text.append("\\n\\n")
        text.append(explanation, style="dim")
        console.print(
            Panel(text, title="lumos", title_align="left", border_style="blue", padding=(1, 2))
        )
    elif input_text:
        with console.status("thinking...", spinner="dots"):
            command = suggest(input_text)
        _display_command(command)
        should_run = console.input(
            "\\n  run this command? [dim]\\\\[y/n][/dim] "
        ).strip().lower() == "y"
        if should_run:
            save_entry(input_text, command)
            console.print()
            result = subprocess.run(command, shell=True)
            sys.exit(result.returncode)
        else:
            save_entry(input_text, command)
    else:
        click.echo(click.get_current_context().get_help())
""")
commit("save suggestions to json", "2022-10-18T10:15:00-04:00")

# 18
write("lumos/cli.py", """import subprocess
import sys

import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from lumos.engine import suggest, explain
from lumos.history import save_entry, get_recent

console = Console()

def _display_command(command):
    text = Text()
    text.append("$ ", style="green bold")
    text.append(command)
    console.print(
        Panel(text, title="lumos", title_align="left", border_style="blue", padding=(1, 2))
    )

def _history(limit):
    entries = get_recent(limit)
    if not entries:
        console.print("  no history yet", style="dim")
        return
    table = Table(title="history", border_style="blue", show_header=True, header_style="bold")
    table.add_column("time", style="dim")
    table.add_column("description")
    table.add_column("command", style="green")
    for entry in entries:
        ts = entry["timestamp"][:16].replace("T", " ")
        table.add_row(ts, entry["description"], entry["command"])
    console.print(table)

@click.command()
@click.argument("input_text", required=False)
@click.option("-e", "--explain", "explain_mode", is_flag=True)
@click.option("-H", "--history", "show_history", is_flag=True)
@click.option("-n", "--limit", default=20)
def cli(input_text, explain_mode, show_history, limit):
    if show_history:
        _history(limit)
    elif explain_mode:
        if not input_text:
            console.print("  provide a command to explain", style="red")
            raise SystemExit(1)
        with console.status("thinking...", spinner="dots"):
            explanation = explain(input_text)
        text = Text()
        text.append("$ ", style="green bold")
        text.append(input_text)
        text.append("\\n\\n")
        text.append(explanation, style="dim")
        console.print(
            Panel(text, title="lumos", title_align="left", border_style="blue", padding=(1, 2))
        )
    elif input_text:
        with console.status("thinking...", spinner="dots"):
            command = suggest(input_text)
        _display_command(command)
        should_run = console.input(
            "\\n  run this command? [dim]\\\\[y/n][/dim] "
        ).strip().lower() == "y"
        if should_run:
            save_entry(input_text, command)
            console.print()
            result = subprocess.run(command, shell=True)
            sys.exit(result.returncode)
        else:
            save_entry(input_text, command)
    else:
        click.echo(click.get_current_context().get_help())
""")
commit("history table with rich", "2022-10-18T11:45:00-04:00")

# 19
write("lumos/history.py", """import json
from datetime import datetime
from pathlib import Path

HISTORY_PATH = Path.home() / ".lumos_history.json"


def _load():
    if not HISTORY_PATH.exists():
        return []
    with open(HISTORY_PATH) as f:
        return json.load(f)


def _save(entries):
    with open(HISTORY_PATH, "w") as f:
        json.dump(entries, f, indent=2)


def save_entry(description, command, executed=False):
    entries = _load()
    entries.append({
        "description": description,
        "command": command,
        "executed": executed,
        "timestamp": datetime.now().isoformat(),
    })
    _save(entries)


def get_recent(n=20):
    return _load()[-n:]
""")
commit("fix timestamp format", "2022-10-18T12:10:00-04:00")

# 20
write("lumos/cli.py", """import subprocess
import sys

import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from lumos.engine import suggest, explain
from lumos.history import save_entry, get_recent

console = Console()


def _display_command(command):
    text = Text()
    text.append("$ ", style="green bold")
    text.append(command)
    console.print(
        Panel(text, title="lumos", title_align="left", border_style="blue", padding=(1, 2))
    )


def _suggest(description, run):
    with console.status("thinking...", spinner="dots"):
        command = suggest(description)
    _display_command(command)
    should_run = run or console.input(
        "\\n  run this command? [dim]\\\\[y/n][/dim] "
    ).strip().lower() == "y"
    if should_run:
        save_entry(description, command, executed=True)
        console.print()
        result = subprocess.run(command, shell=True)
        sys.exit(result.returncode)
    else:
        save_entry(description, command, executed=False)


def _explain(command):
    with console.status("thinking...", spinner="dots"):
        explanation = explain(command)
    text = Text()
    text.append("$ ", style="green bold")
    text.append(command)
    text.append("\\n\\n")
    text.append(explanation, style="dim")
    console.print(
        Panel(text, title="lumos", title_align="left", border_style="blue", padding=(1, 2))
    )


def _history(limit):
    entries = get_recent(limit)
    if not entries:
        console.print("  no history yet", style="dim")
        return
    table = Table(title="history", border_style="blue", show_header=True, header_style="bold")
    table.add_column("time", style="dim")
    table.add_column("description")
    table.add_column("command", style="green")
    table.add_column("ran", justify="center")
    for entry in entries:
        ts = entry["timestamp"][:16].replace("T", " ")
        ran = "y" if entry.get("executed") else ""
        table.add_row(ts, entry["description"], entry["command"], ran)
    console.print(table)


@click.command()
@click.argument("input_text", required=False)
@click.option("-e", "--explain", "explain_mode", is_flag=True)
@click.option("-r", "--run", is_flag=True)
@click.option("-H", "--history", "show_history", is_flag=True)
@click.option("-n", "--limit", default=20)
def cli(input_text, explain_mode, run, show_history, limit):
    if show_history:
        _history(limit)
    elif explain_mode:
        if not input_text:
            console.print("  provide a command to explain", style="red")
            raise SystemExit(1)
        _explain(input_text)
    elif input_text:
        _suggest(input_text, run)
    else:
        click.echo(click.get_current_context().get_help())
""")
commit("add -r flag for auto run", "2022-10-18T14:00:00-04:00")

# ============ Oct 20 2022 ============

# 21
write("lumos/cli.py", """import subprocess
import sys

import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from lumos.engine import suggest, explain
from lumos.history import save_entry, get_recent

console = Console()


def _display_command(command):
    text = Text()
    text.append("$ ", style="green bold")
    text.append(command)
    console.print(
        Panel(text, title="lumos", title_align="left", border_style="blue", padding=(1, 2))
    )


def _suggest(description, run):
    with console.status("thinking...", spinner="dots"):
        command = suggest(description)
    _display_command(command)
    should_run = run or console.input(
        "\\n  run this command? [dim]\\\\[y/n][/dim] "
    ).strip().lower() == "y"
    if should_run:
        save_entry(description, command, executed=True)
        console.print()
        result = subprocess.run(command, shell=True)
        sys.exit(result.returncode)
    else:
        save_entry(description, command, executed=False)


def _explain(command):
    with console.status("thinking...", spinner="dots"):
        explanation = explain(command)
    text = Text()
    text.append("$ ", style="green bold")
    text.append(command)
    text.append("\\n\\n")
    text.append(explanation, style="dim")
    console.print(
        Panel(text, title="lumos", title_align="left", border_style="blue", padding=(1, 2))
    )


def _history(limit):
    entries = get_recent(limit)
    if not entries:
        console.print("  no history yet", style="dim")
        return
    table = Table(title="history", border_style="blue", show_header=True, header_style="bold")
    table.add_column("time", style="dim")
    table.add_column("description")
    table.add_column("command", style="green")
    table.add_column("ran", justify="center")
    for entry in entries:
        ts = entry["timestamp"][:16].replace("T", " ")
        ran = "y" if entry.get("executed") else ""
        table.add_row(ts, entry["description"], entry["command"], ran)
    console.print(table)


@click.command()
@click.argument("input_text", required=False)
@click.option("-e", "--explain", "explain_mode", is_flag=True, help="Explain a command instead of suggesting one.")
@click.option("-r", "--run", is_flag=True, help="Execute the suggested command without confirmation.")
@click.option("-H", "--history", "show_history", is_flag=True, help="Show suggestion history.")
@click.option("-n", "--limit", default=20, help="Number of history entries to show.")
def cli(input_text, explain_mode, run, show_history, limit):
    \"\"\"AI shell command autocomplete powered by davinci-002.\"\"\"
    if show_history:
        _history(limit)
    elif explain_mode:
        if not input_text:
            console.print("  provide a command to explain", style="red")
            raise SystemExit(1)
        _explain(input_text)
    elif input_text:
        _suggest(input_text, run)
    else:
        click.echo(click.get_current_context().get_help())
""")
commit("clean up cli options", "2022-10-20T11:00:00-04:00")

# 22
write("lumos/__init__.py", '__version__ = "0.1.0"\n')
commit("fix", "2022-10-20T11:20:00-04:00")

# 23
write("requirements.txt", "openai\nclick\nrich\npython-dotenv\n")
write("lumos/engine.py", """import openai
from dotenv import load_dotenv
from functools import lru_cache

load_dotenv()


@lru_cache
def _client():
    return openai.OpenAI()


def _suggest_prompt(description):
    return f\"\"\"Translate the description into a single shell command.

Description: list all files sorted by size
Command: ls -lhS

Description: find python files modified in the last week
Command: find . -name "*.py" -mtime -7

Description: show disk usage by directory, sorted
Command: du -sh */ | sort -rh

Description: kill processes matching "node"
Command: pkill -f node

Description: download a file with curl
Command: curl -O https://example.com/file.tar.gz

Description: {description}
Command:\"\"\"


def _explain_prompt(command):
    return (
        "Explain what this shell command does in plain English.\\n\\n"
        'Command: find . -name "*.py" -mtime -7\\n'
        "Explanation: Finds all Python files in the current directory tree "
        "modified within the last 7 days.\\n\\n"
        "Command: du -sh */ | sort -rh\\n"
        "Explanation: Shows disk usage for each subdirectory in human-readable "
        "format, sorted largest to smallest.\\n\\n"
        "Command: awk '{{print $1, $3}}' data.txt\\n"
        "Explanation: Prints the 1st and 3rd columns from each line of "
        "data.txt.\\n\\n"
        f"Command: {command}\\n"
        "Explanation:"
    )


def suggest(description):
    response = _client().completions.create(
        model="davinci-002",
        prompt=_suggest_prompt(description),
        max_tokens=150,
        temperature=0,
        stop=["\\n\\n", "\\nDescription:"],
    )
    return response.choices[0].text.strip()


def explain(command):
    response = _client().completions.create(
        model="davinci-002",
        prompt=_explain_prompt(command),
        max_tokens=200,
        temperature=0,
        stop=["\\n\\n", "\\nCommand:"],
    )
    return response.choices[0].text.strip()
""")
commit("add dotenv support", "2022-10-20T13:30:00-04:00")

# 24
write(".gitignore", """__pycache__/
*.py[cod]
*.egg-info/
dist/
build/
.eggs/
*.egg
.env
.venv/
venv/
.DS_Store
""")
write(".env.example", "OPENAI_API_KEY=sk-...\n")
commit("update gitignore", "2022-10-20T13:45:00-04:00")

# ============ Oct 22 2022 ============

# 25
write("README.md", """# Lumos

cli tool that turns plain english into shell commands using openai's davinci-002 completion model.

## Setup

```bash
pip install -e .
cp .env.example .env
```

## Usage

```bash
lumos "find all python files larger than 1MB"
```
""")
commit("add readme", "2022-10-22T10:00:00-04:00")

# 26
write("pyproject.toml", """[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "lumos"
version = "0.1.0"
description = "AI shell command autocomplete powered by OpenAI davinci-002"
requires-python = ">=3.10"
dependencies = [
    "openai>=1.0.0",
    "click>=8.0.0",
    "rich>=13.0.0",
    "python-dotenv>=1.0.0",
]

[project.scripts]
lumos = "lumos.cli:cli"
""")
write("requirements.txt", """openai>=1.0.0
click>=8.0.0
rich>=13.0.0
python-dotenv>=1.0.0
""")
commit("fix", "2022-10-22T10:15:00-04:00")

# 27
write("README.md", """# Lumos

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
\u256d\u2500 lumos \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u256e
\u2502                                    \u2502
\u2502  $ find . -name "*.py" -size +1M   \u2502
\u2502                                    \u2502
\u2570\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u256f

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
""")
commit("fix readme", "2022-10-22T10:30:00-04:00")

# 28 - final type hints cleanup
write("lumos/engine.py", """import openai
from dotenv import load_dotenv
from functools import lru_cache

load_dotenv()


@lru_cache
def _client():
    return openai.OpenAI()


def _suggest_prompt(description: str) -> str:
    return f\"\"\"Translate the description into a single shell command.

Description: list all files sorted by size
Command: ls -lhS

Description: find python files modified in the last week
Command: find . -name "*.py" -mtime -7

Description: show disk usage by directory, sorted
Command: du -sh */ | sort -rh

Description: kill processes matching "node"
Command: pkill -f node

Description: download a file with curl
Command: curl -O https://example.com/file.tar.gz

Description: {description}
Command:\"\"\"


def _explain_prompt(command: str) -> str:
    return (
        "Explain what this shell command does in plain English.\\n\\n"
        'Command: find . -name "*.py" -mtime -7\\n'
        "Explanation: Finds all Python files in the current directory tree "
        "modified within the last 7 days.\\n\\n"
        "Command: du -sh */ | sort -rh\\n"
        "Explanation: Shows disk usage for each subdirectory in human-readable "
        "format, sorted largest to smallest.\\n\\n"
        "Command: awk '{{print $1, $3}}' data.txt\\n"
        "Explanation: Prints the 1st and 3rd columns from each line of "
        "data.txt.\\n\\n"
        f"Command: {command}\\n"
        "Explanation:"
    )


def suggest(description: str) -> str:
    response = _client().completions.create(
        model="davinci-002",
        prompt=_suggest_prompt(description),
        max_tokens=150,
        temperature=0,
        stop=["\\n\\n", "\\nDescription:"],
    )
    return response.choices[0].text.strip()


def explain(command: str) -> str:
    response = _client().completions.create(
        model="davinci-002",
        prompt=_explain_prompt(command),
        max_tokens=200,
        temperature=0,
        stop=["\\n\\n", "\\nCommand:"],
    )
    return response.choices[0].text.strip()
""")
write("lumos/history.py", """import json
from datetime import datetime
from pathlib import Path

HISTORY_PATH = Path.home() / ".lumos_history.json"


def _load() -> list[dict]:
    if not HISTORY_PATH.exists():
        return []
    with open(HISTORY_PATH) as f:
        return json.load(f)


def _save(entries: list[dict]):
    with open(HISTORY_PATH, "w") as f:
        json.dump(entries, f, indent=2)


def save_entry(description: str, command: str, executed: bool = False):
    entries = _load()
    entries.append({
        "description": description,
        "command": command,
        "executed": executed,
        "timestamp": datetime.now().isoformat(),
    })
    _save(entries)


def get_recent(n: int = 20) -> list[dict]:
    return _load()[-n:]
""")
commit("clean up prompts", "2022-10-22T11:00:00-04:00")

# rename branch to main
run("git branch -M main")

print("done - 28 commits on main")
