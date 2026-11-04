# language: ja
機能: TODOの追加と完了（server-medium / API+SQLiteで観測）

  # 同じ振る舞いを「API レスポンス＋DB」で観測する
  @SYS-UC-TODO-01-001 @server-medium
  シナリオ: 空のリストに項目を追加する
    前提 TODOリストが空である
    もし 「牛乳を買う」を追加する
    ならば リストに「牛乳を買う」が1件表示される

  @SYS-UC-TODO-01-002 @server-medium
  シナリオ: 項目を完了にする
    前提 「牛乳を買う」が未完了で1件ある
    もし その項目を完了にする
    ならば その項目が完了状態になり、未完了件数が0件になる
