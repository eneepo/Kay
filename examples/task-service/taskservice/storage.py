"""storage — load and save the task list as JSON.

A missing file is treated as an empty store. A corrupt file is a clear error,
never a silent wipe.
"""
import json
from pathlib import Path


class StorageError(Exception):
    """Raised when the store file exists but cannot be read as a task list."""


def load(path):
    """Return the task list stored at `path`, or [] if the file does not exist."""
    p = Path(path)
    if not p.exists():
        return []
    try:
        data = json.loads(p.read_text())
    except (json.JSONDecodeError, ValueError) as exc:
        raise StorageError(f"{path} is not valid JSON: {exc}") from exc
    if not isinstance(data, list):
        raise StorageError(f"{path} does not contain a task list")
    return data


def save(path, tasks):
    """Write the task list to `path` as pretty JSON."""
    Path(path).write_text(json.dumps(tasks, indent=2))
