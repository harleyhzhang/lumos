import openai
from dotenv import load_dotenv
from functools import lru_cache

load_dotenv()


@lru_cache
def _client():
    return openai.OpenAI()


def _suggest_prompt(description):
    return f"""Translate the description into a single shell command.

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
Command:"""


def _explain_prompt(command):
    return (
        "Explain what this shell command does in plain English.\n\n"
        'Command: find . -name "*.py" -mtime -7\n'
        "Explanation: Finds all Python files in the current directory tree "
        "modified within the last 7 days.\n\n"
        "Command: du -sh */ | sort -rh\n"
        "Explanation: Shows disk usage for each subdirectory in human-readable "
        "format, sorted largest to smallest.\n\n"
        "Command: awk '{{print $1, $3}}' data.txt\n"
        "Explanation: Prints the 1st and 3rd columns from each line of "
        "data.txt.\n\n"
        f"Command: {command}\n"
        "Explanation:"
    )


def suggest(description):
    response = _client().completions.create(
        model="davinci-002",
        prompt=_suggest_prompt(description),
        max_tokens=150,
        temperature=0,
        stop=["\n\n", "\nDescription:"],
    )
    return response.choices[0].text.strip()


def explain(command):
    response = _client().completions.create(
        model="davinci-002",
        prompt=_explain_prompt(command),
        max_tokens=200,
        temperature=0,
        stop=["\n\n", "\nCommand:"],
    )
    return response.choices[0].text.strip()
