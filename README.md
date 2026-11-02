# BDD ハンズオン・キット（TODO / Windows ですぐ動く）

「振る舞いを **usecase.md に書く**」→「そのまま **評価する**」が1本に繋がる体験を、
超簡単な TODO 機能で体感するキットです。node 不要で始められ、同じ振る舞いを
**3つの評価レイヤー**で確かめられます。

## 3つのレイヤー（このキットの地図）

| 評価レイヤー | どこで | 動かし方(Windows) |
| --- | --- | --- |
| **(unit)** 純粋ロジック | `./`（pytest 版）/ `web/index.html` 内の `TodoLogic` | 下記「最短体験」 |
| **(client-medium)** 画面結合 | `web/index.html` / `web-test/`（Playwright） | ダブルクリックで開く。`web-test/` で画面を自動検証 |
| **(server-medium)** API+DB 結合 | `server/`（Flask + SQLite） | `server/README.md` 参照 |

同じ振る舞い「未完了が0件になる」を、unit でも client-medium でも server-medium でも評価できる——
**書く時点でどのレイヤーで評価するか決める**、がこのキットの主役メッセージです。

## 最短体験（pytest 版・node不要）

このフォルダで:

    py -m venv .venv
    .venv\Scripts\activate
    py -m pip install -r requirements.txt
    py -m pytest -q

初回は **1 passed / 1 failed**（完了判定をわざと TODO にしてある）。
`steps\test_todo.py` の最後の TODO 行を

    assert todo.pending_count() == 0

に置き換えて再実行すると **2 passed**。これが「書いた振る舞いが評価になる」瞬間です。

## 画面で見たい（client-medium）

`web/index.html` をダブルクリック → ブラウザで TODO が動きます（依存ゼロ）。詳細は `web/README.md`。

## API+DB で見たい（server-medium）

`server/` で Flask + SQLite 版を起動（`server/README.md`）。DB は SQLite ファイル1個、追加インストール不要。

## 画面を自動テストしたい（client-medium）

`web-test/` で Playwright が実ブラウザを開き「追加→完了→未完了0件」を画面で検証（`web-test/README.md`）。

## ファイル全体図

| 場所 | 役割 |
| --- | --- |
| `PA_TODO_01.usecase.md` | 振る舞いの SSOT（Given/When/Then＋評価レイヤー） |
| `features/` `steps/` `todo.py` | unit の pytest-bdd 一式 |
| `web/index.html` | 単一HTML アプリ（unit ロジック＋画面） |
| `server/app.py` ほか | Flask + SQLite アプリ＋ server-medium テスト |
| `requirements.txt` `pytest.ini` | 依存固定・設定 |

## 備考

- pytest-bdd 9.0.0 は pytest 9 系と非互換のため `pytest>=8,<9` に固定済み。
- 実プロジェクトは `npx tsx` + playwright-bdd（node 必要）。本キットは考え方を同じにしたまま、
  環境でこけないよう Python/単一HTML に寄せた体験版です。
