import pytest

from taskservice import storage


def test_missing_file_is_empty_store(tmp_path):
    assert storage.load(tmp_path / "nope.json") == []


def test_save_then_load_round_trips(tmp_path):
    path = tmp_path / "tasks.json"
    tasks = [{"id": 1, "title": "buy milk", "done": False}]
    storage.save(path, tasks)
    assert storage.load(path) == tasks


def test_corrupt_file_raises(tmp_path):
    path = tmp_path / "tasks.json"
    path.write_text("{not json")
    with pytest.raises(storage.StorageError):
        storage.load(path)


def test_non_list_json_raises(tmp_path):
    path = tmp_path / "tasks.json"
    path.write_text('{"tasks": []}')
    with pytest.raises(storage.StorageError):
        storage.load(path)
