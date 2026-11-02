"""TODO API サーバ (Flask + SQLite)。評価レイヤー = server-medium。

- DB は SQLite(Python標準の sqlite3)。追加インストール不要。
- `py app.py` で http://127.0.0.1:5000 に起動。ブラウザで画面も開ける。
- 同じ画面(web/index.html とほぼ同じ見た目)を配信しつつ、
  追加/完了/削除を API 経由で SQLite に保存する=front↔API↔DB が本物の構造。
"""
import sqlite3
from pathlib import Path
from flask import Flask, g, jsonify, request, Response

DB_PATH = Path(__file__).with_name("todo.db")

app = Flask(__name__)


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(_exc):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    con = sqlite3.connect(DB_PATH)
    con.execute(
        "CREATE TABLE IF NOT EXISTS todos ("
        " id INTEGER PRIMARY KEY AUTOINCREMENT,"
        " title TEXT NOT NULL,"
        " done INTEGER NOT NULL DEFAULT 0)"
    )
    con.commit()
    con.close()


@app.get("/api/todos")
def list_todos():
    rows = get_db().execute("SELECT id, title, done FROM todos ORDER BY id").fetchall()
    items = [{"id": r["id"], "title": r["title"], "done": bool(r["done"])} for r in rows]
    pending = len([i for i in items if not i["done"]])
    return jsonify({"items": items, "pending": pending, "total": len(items)})


@app.post("/api/todos")
def add_todo():
    title = (request.get_json(silent=True) or {}).get("title", "")
    title = str(title).strip()
    if title == "":
        # 空タイトルは登録しない(準正常)
        return jsonify({"error": "title is required"}), 400
    db = get_db()
    db.execute("INSERT INTO todos (title, done) VALUES (?, 0)", (title,))
    db.commit()
    return list_todos()


@app.patch("/api/todos/<int:todo_id>")
def toggle_todo(todo_id):
    db = get_db()
    row = db.execute("SELECT done FROM todos WHERE id = ?", (todo_id,)).fetchone()
    if row is None:
        return jsonify({"error": "not found"}), 404
    db.execute("UPDATE todos SET done = ? WHERE id = ?", (0 if row["done"] else 1, todo_id))
    db.commit()
    return list_todos()


@app.delete("/api/todos/<int:todo_id>")
def delete_todo(todo_id):
    db = get_db()
    db.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
    db.commit()
    return list_todos()


@app.get("/")
def index():
    return Response(PAGE, mimetype="text/html")


# 画面は単一HTML版と同等。API 経由で SQLite に保存する点だけ違う。
PAGE = """<!DOCTYPE html>
<html lang="ja"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>My TODO (Flask + SQLite版)</title>
<style>
 :root{--bg:#f4f5f7;--card:#fff;--fg:#1a1d23;--muted:#6b7280;--border:#e2e5ea;--primary:#2563eb;--primary-fg:#fff}
 *{box-sizing:border-box}body{font-family:system-ui,-apple-system,"Segoe UI",sans-serif;background:var(--bg);color:var(--fg);margin:0;padding:32px 16px}
 .card{max-width:520px;margin:0 auto;background:var(--card);border:1px solid var(--border);border-radius:14px;padding:24px 26px;box-shadow:0 2px 12px rgba(0,0,0,.08)}
 h1{margin:0 0 2px;font-size:22px}.counter{margin:0 0 18px;font-size:13px;color:var(--muted)}.counter strong{color:var(--fg)}
 .input-row{display:flex;gap:8px;margin-bottom:18px}#title{flex:1;padding:9px 12px;border:1px solid var(--border);border-radius:8px;font-size:14px}
 #add{padding:9px 18px;border:none;border-radius:8px;background:var(--primary);color:var(--primary-fg);font-size:14px;font-weight:600;cursor:pointer}
 ul{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:8px}
 li{display:flex;align-items:center;gap:10px;padding:10px 12px;border:1px solid var(--border);border-radius:9px}
 li.done{opacity:.65;background:#fafafa}li.done .title{text-decoration:line-through;color:var(--muted)}
 .title{flex:1;font-size:14.5px}.del{padding:4px 10px;border:1px solid var(--border);border-radius:6px;background:transparent;color:var(--muted);font-size:12px;cursor:pointer}
 .empty{color:var(--muted);font-size:13px;padding:8px 2px}
</style></head><body>
<div class="card">
 <h1>📝 My TODO <span style="font-size:12px;color:var(--muted)">(API+SQLite)</span></h1>
 <p class="counter">未完了 <strong id="pending">0</strong> 件 / 全 <span id="total">0</span> 件</p>
 <div class="input-row"><input id="title" placeholder="やることを入力…" autocomplete="off"><button id="add">追加</button></div>
 <ul id="list"></ul>
</div>
<script>
 const $=(id)=>document.getElementById(id);
 async function api(method,path,body){const r=await fetch(path,{method,headers:{"Content-Type":"application/json"},body:body?JSON.stringify(body):undefined});return r.ok?r.json():null;}
 function render(d){const list=$("list");list.innerHTML="";if(!d.items.length){const li=document.createElement("li");li.className="empty";li.textContent="まだ何もありません。上の欄から追加してください。";list.appendChild(li);}
  for(const it of d.items){const li=document.createElement("li");li.className=it.done?"done":"";li.dataset.title=it.title;
   const cb=document.createElement("input");cb.type="checkbox";cb.checked=it.done;cb.setAttribute("aria-label","完了にする: "+it.title);
   cb.addEventListener("change",async()=>render(await api("PATCH","/api/todos/"+it.id)));
   const span=document.createElement("span");span.className="title";span.textContent=it.title;
   const del=document.createElement("button");del.className="del";del.textContent="削除";
   del.addEventListener("click",async()=>render(await api("DELETE","/api/todos/"+it.id)));
   li.append(cb,span,del);list.appendChild(li);}
  $("pending").textContent=d.pending;$("total").textContent=d.total;}
 async function reload(){render(await api("GET","/api/todos"));}
 $("add").addEventListener("click",async()=>{const t=$("title").value;const d=await api("POST","/api/todos",{title:t});$("title").value="";if(d)render(d);});
 $("title").addEventListener("keydown",(e)=>{if(e.key==="Enter")$("add").click();});
 reload();
</script></body></html>
"""

if __name__ == "__main__":
    init_db()
    # 127.0.0.1 のみにバインド(社内でも安全)
    app.run(host="127.0.0.1", port=5000, debug=False)
