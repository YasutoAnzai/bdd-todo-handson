# B: Flask + SQLite 版 TODO アプリ（server-medium 用）

front↔API↔DB が本物の構造で動きます。DB は **SQLite（Python標準の `sqlite3`）**＝追加インストール不要、
ファイル1個（`todo.db`）がDBです。PostgreSQL は使いません。

## 起動（Windows・コピペ）

このフォルダ（`server/`）で:

    py -m venv .venv
    .venv\Scripts\activate
    py -m pip install -r requirements.txt
    py app.py

起動したらブラウザで http://127.0.0.1:5000 を開く。追加・完了・削除が **API 経由で SQLite に保存**されます。
止めるときは実行中のウィンドウで Ctrl+C。

> PowerShell で activate が実行ポリシーで止まる場合は、有効化せず
> `.venv\Scripts\python.exe app.py` でも起動できます。

## BDD（server-medium）テストの実行

    py -m pytest -q

- 2 つのシナリオ（API で追加→一覧に1件 / API で完了→未完了0件）が **2 passed** になれば成功。
- テストは Flask のテストクライアント経由で API を叩き、**各テストごとに一時 SQLite** を使う
  （＝Given「DBが空」を毎回クリーンに作る）。

## 構成

| ファイル | 役割 |
| --- | --- |
| `app.py` | Flask API（`/api/todos` の GET/POST/PATCH/DELETE）＋ 画面配信。DB は SQLite |
| `features\todo_api.feature` | 日本語 Gherkin（server-medium の振る舞い） |
| `steps\test_todo_api.py` | ステップ定義。API→実DB→API を検証 |
| `requirements.txt` | flask / pytest / pytest-bdd（バージョン固定） |

## BDD での位置づけ

評価レイヤー **(server-medium)**。A（単一HTML）と**同じ振る舞い**を、今度は
「API を叩いて SQLite に正しく保存・集計されたか」で評価します。実プロジェクト（Next + API + DB）に
一番近い形で、「同じ Given/When/Then が層をまたいで評価できる」を体験できます。
