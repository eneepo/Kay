import pytest

from taskservice import domain


def test_add_assigns_incrementing_ids():
    tasks = []
    first = domain.add(tasks, "one")
    second = domain.add(tasks, "two")
    assert first["id"] == 1
    assert second["id"] == 2
    assert [t["title"] for t in tasks] == ["one", "two"]


def test_add_rejects_empty_title():
    with pytest.raises(domain.TaskError):
        domain.add([], "   ")


def test_complete_marks_done():
    tasks = []
    domain.add(tasks, "one")
    domain.complete(tasks, 1)
    assert tasks[0]["done"] is True


def test_complete_unknown_id_raises():
    with pytest.raises(domain.TaskError):
        domain.complete([], 99)


def test_delete_removes_task():
    tasks = []
    domain.add(tasks, "one")
    domain.delete(tasks, 1)
    assert tasks == []


def test_list_filters_by_status():
    tasks = []
    domain.add(tasks, "todo-one")
    domain.add(tasks, "done-one")
    domain.complete(tasks, 2)
    assert [t["id"] for t in domain.list_tasks(tasks, "todo")] == [1]
    assert [t["id"] for t in domain.list_tasks(tasks, "done")] == [2]
    assert len(domain.list_tasks(tasks)) == 2
