"""usecase.md の Given/When/Then が、そのまま step になる。"""
import sys
from pathlib import Path

from pytest_bdd import scenarios, given, when, then, parsers

# このファイルの位置を基準に解決する(どこから pytest を起動しても壊れない)
_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_ROOT))
from todo import TodoList

scenarios(str(_ROOT / "features" / "todo.feature"))


@given("TODOリストが空である", target_fixture="todo")
def empty_list():
    return TodoList()


@given('「牛乳を買う」が未完了で1件ある', target_fixture="todo")
def one_pending():
    t = TodoList()
    t.add("牛乳を買う")
    return t


@when('「牛乳を買う」を追加する')
def add_milk(todo):
    todo.add("牛乳を買う")


@when("その項目を完了にする")
def complete_it(todo):
    todo.complete("牛乳を買う")


@then('リストに「牛乳を買う」が1件表示される')
def shown_once(todo):
    assert todo.titles() == ["牛乳を買う"]


@then("未完了の件数が0件になる")
def pending_zero(todo):
    # TODO(ハンズオン): ここを1行実装してください。
    #   ヒント: todo.pending_count() が 0 であることを assert する
    raise NotImplementedError("ここを実装すると緑になります")
