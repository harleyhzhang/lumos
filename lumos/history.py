import json
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
