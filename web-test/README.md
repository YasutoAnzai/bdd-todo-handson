# client-medium: 画面テスト（Playwright / ブラウザ操作）

単一HTML版 `../web/index.html` を**実ブラウザで開いて操作し、画面の表示で振る舞いを検証**します。
評価レイヤー = **(client-medium)**。node は不要（Python の Playwright がブラウザを同梱）。

## 実行（Windows・コピペ）

このフォルダ（`web-test/`）で:

    py -m venv .venv
    .venv\Scripts\activate
    py -m pip install -r requirements.txt
    py -m playwright install chromium
    py -m pytest -q --headed --slowmo 3000

**1 passed** になれば成功。
（`playwright install chromium` は初回だけ。ブラウザ本体をダウンロードします。社内プロキシ環境では
 これだけネットワーク許可が要る場合があります。）

## 何を検証しているか

| | 内容 |
| --- | --- |
| 前提(Given) | TODO画面を空の状態で開いている（localStorage をクリア） |
| トリガー(When) | 「牛乳を買う」を追加してチェックで完了にする |
| 概要(Then) | **画面の**未完了件数が 0 件になり、完了行に取り消し線が付く |

## BDD での位置づけ

同じ振る舞い「未完了が0件になる」を、
- unit（`todo.py` の `pending_count()==0`）
- server-medium（API+SQLite の `pending==0`）
- **client-medium（この画面テスト：`#pending` の表示が 0）** ←ここ

の3通りで評価できる。**観測点が「ユーザーが見る画面」**である点が client-medium の肝です。
