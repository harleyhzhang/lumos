import json
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
