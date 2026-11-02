# BDD ハンズオン・キット（TODOシステム / Windows ですぐ動く）

「振る舞いを書く（usecase.md）」→「評価する（テスト）」が1本に繋がる体験を、
超簡単な TODO 機能で 5 分体感するキットです。node 不要・Python だけ。

## 用意するもの

- Windows + Python 3.10 以上（`py --version` で確認。無ければ https://www.python.org/ から入れる／社内手順に従う）
- このフォルダ一式

## 手順（PowerShell か コマンドプロンプトに貼るだけ）

このフォルダで以下を順に実行します。

    py -m venv .venv
    .venv\Scripts\activate
    py -m pip install -r requirements.txt
    py -m pytest -q

PowerShell で activate が実行ポリシーで止まる場合は、有効化せずそのまま
`.venv\Scripts\python.exe -m pytest -q` でも動きます。

### 1 回目の実行結果（これが正しい）

    1 passed, 1 failed

- passed＝「追加」の振る舞いは実装済みで緑。
- failed＝「完了件数が0件になる」の判定を **わざと TODO（未実装）** にしてあります。

### あなたのタスク（1 行だけ）

steps\test_todo.py の一番下 pending_zero 関数の TODO 行を、次の 1 行に置き換えます。

    assert todo.pending_count() == 0

（元の raise NotImplementedError(...) を消して上の 1 行にする）

### もう一度実行

    py -m pytest -q
    2 passed

緑になりました。usecase.md に書いた日本語の振る舞いが、そのままテストになって評価された——これが BDD の肝です。

## ファイルの地図

| ファイル | 役割 |
| --- | --- |
| PA_TODO_01.usecase.md | 振る舞いの SSOT。前提=Given / トリガー=When / 概要=Then、備考に評価レイヤー |
| features\todo.feature | 日本語 Gherkin（# language: ja）。usecase.md の各行がそのまま写っている |
| steps\test_todo.py | ステップ定義。Given/When/Then と同じ文が関数に紐づく（1 箇所 TODO） |
| todo.py | 本番ロジック（外部 I/O なしの純粋関数＝評価レイヤーは unit） |
| requirements.txt | 依存のバージョン固定（pytest 8 系 / pytest-bdd 9.0.0） |
| pytest.ini | feature の場所と警告抑制 |

## なぜこの題材・この構成か

- TODO は全員が仕様を 3 秒で理解できる題材。BDD の「書く↔評価」の構造だけに集中できる。
- 実プロジェクトは npx tsx + playwright-bdd（node 必要）。環境未整備の人が 15 分を環境構築で溶かさないよう、考え方が 100% 同じ pytest-bdd（Python）で体験部分だけ切り出し。
- pytest-bdd 9.0.0 は pytest 9 系と非互換なので pytest>=8,<9 に固定済み（罠を踏まない）。
