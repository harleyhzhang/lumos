import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")


def _suggest_prompt(description):
    return f"""Translate the description into a single shell command.

Description: list all files sorted by size
Command: ls -lhS

Description: find python files modified in the last week
Command: find . -name "*.py" -mtime -7

Description: show disk usage by directory, sorted
Command: du -sh */ | sort -rh

Description: {description}
Command:"""


def suggest(description):
    response = openai.Completion.create(
        model="davinci-002",
        prompt=_suggest_prompt(description),
        max_tokens=150,
        temperature=0,
    )
    return response.choices[0].text.strip()
