from taskservice import api


def test_get_empty_returns_empty_list(tmp_path):
    status, payload = api.dispatch("GET", "/tasks", None, tmp_path / "t.json")
    assert status == 200
    assert payload == []


def test_post_creates_task(tmp_path):
    file = tmp_path / "t.json"
    status, payload = api.dispatch("POST", "/tasks", {"title": "buy milk"}, file)
    assert status == 201
    assert payload["id"] == 1 and payload["title"] == "buy milk"
    # persisted: a follow-up GET sees it
    _, listed = api.dispatch("GET", "/tasks", None, file)
    assert [t["id"] for t in listed] == [1]


def test_post_empty_title_is_400(tmp_path):
    status, payload = api.dispatch("POST", "/tasks", {"title": ""}, tmp_path / "t.json")
    assert status == 400
    assert "error" in payload


def test_delete_unknown_is_404(tmp_path):
    status, payload = api.dispatch("DELETE", "/tasks/99", None, tmp_path / "t.json")
    assert status == 404


def test_delete_existing(tmp_path):
    file = tmp_path / "t.json"
    api.dispatch("POST", "/tasks", {"title": "one"}, file)
    status, payload = api.dispatch("DELETE", "/tasks/1", None, file)
    assert status == 200 and payload == {"deleted": 1}
    _, listed = api.dispatch("GET", "/tasks", None, file)
    assert listed == []


def test_get_status_filter(tmp_path):
    file = tmp_path / "t.json"
    api.dispatch("POST", "/tasks", {"title": "one"}, file)
    api.dispatch("POST", "/tasks", {"title": "two"}, file)
    status, payload = api.dispatch("GET", "/tasks?status=todo", None, file)
    assert status == 200 and len(payload) == 2
