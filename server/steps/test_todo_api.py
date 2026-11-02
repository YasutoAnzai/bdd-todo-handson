"""server-medium の BDD ステップ。

Flask のテストクライアント経由で API を叩き、実際の SQLite(一時DB)に保存される。
Given(前提)= 一時DBを初期化する、という形で状態を作る点がポイント。
"""
import importlib
import sqlite3
import sys
from pathlib import Path

import pytest
from pytest_bdd import scenarios, given, when, then

# server/app.py を import できるようにする
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

scenarios(str(Path(__file__).resolve().parents[1] / "features" / "todo_api.feature"))


@pytest.fixture
def app(tmp_path, monkeypatch):
    """各テストごとに新しい SQLite ファイルを使う(=Given:DBが空 を保証)。"""
    import app as app_module
    importlib.reload(app_module)
    db_file = tmp_path / "todo.db"
    monkeypatch.setattr(app_module, "DB_PATH", db_file)
    app_module.init_db()
    app_module.app.config.update(TESTING=True)
    return app_module.app


@pytest.fixture
def client(app):
    return app.test_client()


@given("DBが空である")
def db_empty(client):
    res = client.get("/api/todos").get_json()
    assert res["total"] == 0


@given('「牛乳を買う」が未完了で1件ある')
def one_pending(client):
    client.post("/api/todos", json={"title": "牛乳を買う"})


@when('APIで「牛乳を買う」を追加する')
def add_via_api(client):
    client.post("/api/todos", json={"title": "牛乳を買う"})


@when("その項目をAPIで完了にする")
def complete_via_api(client):
    todos = client.get("/api/todos").get_json()["items"]
    target = todos[0]["id"]
    client.patch(f"/api/todos/{target}")


@then('一覧に「牛乳を買う」が1件返る')
def one_milk(client):
    res = client.get("/api/todos").get_json()
    titles = [i["title"] for i in res["items"]]
    assert titles == ["牛乳を買う"]


@then("未完了の件数が0件になる")
def pending_zero(client):
    res = client.get("/api/todos").get_json()
    assert res["pending"] == 0
