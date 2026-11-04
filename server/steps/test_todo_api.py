"""server-medium の BDD ステップ（Flask テストクライアント + 実 SQLite）。

評価レイヤー = server-medium。観測点 = API レスポンス＋DB(一時SQLite)。
unit / client-medium と **同じ Given/When/Then** を、ここでは API+DB で観測する。
Given(前提) = 一時DBを初期化する、という形で状態を作る。
"""
import importlib
import sys
from pathlib import Path

import pytest
from pytest_bdd import scenarios, given, when, then

# server/app.py を import できるようにする
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

scenarios(str(Path(__file__).resolve().parents[1] / "features" / "todo_api.feature"))


@pytest.fixture
def client(tmp_path, monkeypatch):
    """各テストごとに新しい SQLite ファイルを使う(=空DBを保証)。"""
    import app as app_module
    importlib.reload(app_module)
    monkeypatch.setattr(app_module, "DB_PATH", tmp_path / "todo.db")
    app_module.init_db()
    app_module.app.config.update(TESTING=True)
    return app_module.app.test_client()


@given("TODOリストが空である", target_fixture="todo_client")
def empty_db(client):
    assert client.get("/api/todos").get_json()["total"] == 0
    return client


@given('「牛乳を買う」が未完了で1件ある', target_fixture="todo_client")
def one_pending(client):
    client.post("/api/todos", json={"title": "牛乳を買う"})
    return client


@when('「牛乳を買う」を追加する')
def add_milk(todo_client):
    todo_client.post("/api/todos", json={"title": "牛乳を買う"})


@when("その項目を完了にする")
def complete_it(todo_client):
    todos = todo_client.get("/api/todos").get_json()["items"]
    todo_client.patch(f"/api/todos/{todos[0]['id']}")


@then('リストに「牛乳を買う」が1件表示される')
def one_milk(todo_client):
    titles = [i["title"] for i in todo_client.get("/api/todos").get_json()["items"]]
    assert titles == ["牛乳を買う"]


@then("その項目が完了状態になり、未完了件数が0件になる")
def pending_zero(todo_client):
    assert todo_client.get("/api/todos").get_json()["pending"] == 0
