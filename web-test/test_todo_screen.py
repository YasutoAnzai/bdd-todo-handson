"""client-medium の BDD テスト（Playwright でブラウザ操作）。

評価レイヤー = client-medium。
単一HTML版 `web/index.html` を実ブラウザで開き、画面を操作して
「未完了が0件になる」を *画面の表示* で検証する。

同じ振る舞いを unit（todo.py の pendingCount）/ server-medium（API+SQLite）でも
評価できるが、ここでは「ユーザーが見る画面」を観測点にする点がポイント。

実行(Windows):
    py -m venv .venv
    .venv\\Scripts\\activate
    py -m pip install -r requirements.txt
    py -m playwright install chromium
    py -m pytest -q
"""
from pathlib import Path

import pytest
from pytest_bdd import scenarios, given, when, then

INDEX = (Path(__file__).resolve().parents[1] / "web" / "index.html").as_uri()

scenarios("../features/todo_screen.feature")


@pytest.fixture
def todo_page(page):
    # Given の土台: localStorage をクリアしてから空の状態で開く
    page.goto(INDEX)
    page.evaluate("localStorage.clear()")
    page.goto(INDEX)
    return page


@given("TODO画面を空の状態で開いている")
def opened_empty(todo_page):
    assert todo_page.locator("#pending").inner_text() == "0"


@when('「牛乳を買う」を追加して完了にする')
def add_and_complete(todo_page):
    todo_page.fill("#title", "牛乳を買う")
    todo_page.click("#add")
    # 追加された行のチェックボックスを押して完了にする
    todo_page.locator('li[data-title="牛乳を買う"] input[type="checkbox"]').check()


@then("画面の未完了件数が0件になる")
def pending_zero_on_screen(todo_page):
    assert todo_page.locator("#pending").inner_text() == "0"
    # 完了行は取り消し線クラス(done)が付く
    assert "done" in (todo_page.locator('li[data-title="牛乳を買う"]').get_attribute("class") or "")
