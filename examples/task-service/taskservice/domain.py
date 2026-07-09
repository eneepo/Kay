"""domain — the task operations, independent of any front-end or storage format.

A task is a dict: {"id": int, "title": str, "done": bool}.
Every operation works on a plain list of such dicts, so it is trivial to test.
"""


class TaskError(Exception):
    """Raised on invalid input (e.g. empty title) or an unknown task id."""


def add(tasks, title):
    """Append a new task with the next id and return it. Empty title is rejected."""
    title = (title or "").strip()
    if not title:
        raise TaskError("task title must not be empty")
    new_id = max((t["id"] for t in tasks), default=0) + 1
    task = {"id": new_id, "title": title, "done": False}
    tasks.append(task)
    return task


def get(tasks, task_id):
    """Return the task with `task_id`, or raise TaskError if there is none."""
    for task in tasks:
        if task["id"] == task_id:
            return task
    raise TaskError(f"no task with id {task_id}")


def complete(tasks, task_id):
    """Mark the task done and return it."""
    task = get(tasks, task_id)
    task["done"] = True
    return task


def delete(tasks, task_id):
    """Remove the task and return it."""
    task = get(tasks, task_id)
    tasks.remove(task)
    return task


def list_tasks(tasks, status=None):
    """Return tasks, optionally filtered by status ("todo" or "done")."""
    if status is None:
        return list(tasks)
    if status == "todo":
        return [t for t in tasks if not t["done"]]
    if status == "done":
        return [t for t in tasks if t["done"]]
    raise TaskError(f"unknown status filter: {status}")
