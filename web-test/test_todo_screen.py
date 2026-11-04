"""client-medium の BDD テスト（Playwright でブラウザ操作）。

評価レイヤー = client-medium。観測点 = ユーザーが見る *画面の表示*。
unit（todo.py）/ server-medium（API+SQLite）と **同じ Given/When/Then** を、
ここではブラウザ上で観測する。

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

scenarios(str(Path(__file__).resolve().parent / "features" / "todo_screen.feature"))


def _open_empty(page):
    page.goto(INDEX)
    page.evaluate("localStorage.clear()")
    page.goto(INDEX)
    return page


@given("TODOリストが空である", target_fixture="todo_page")
def empty_screen(page):
    p = _open_empty(page)
    assert p.locator("#pending").inner_text() == "0"
    return p


@given('「牛乳を買う」が未完了で1件ある', target_fixture="todo_page")
def one_pending_screen(page):
    p = _open_empty(page)
    p.fill("#title", "牛乳を買う")
    p.click("#add")
    return p


@when('「牛乳を買う」を追加する')
def add_milk(todo_page):
    todo_page.fill("#title", "牛乳を買う")
    todo_page.click("#add")


@when("その項目を完了にする")
def complete_it(todo_page):
    todo_page.locator('li[data-title="牛乳を買う"] input[type="checkbox"]').check()


@then('リストに「牛乳を買う」が1件表示される')
def shown_once(todo_page):
    rows = todo_page.locator('li[data-title="牛乳を買う"]')
    assert rows.count() == 1


@then("その項目が完了状態になり、未完了件数が0件になる")
def done_and_pending_zero(todo_page):
    assert todo_page.locator("#pending").inner_text() == "0"
    cls = todo_page.locator('li[data-title="牛乳を買う"]').get_attribute("class") or ""
    assert "done" in cls
