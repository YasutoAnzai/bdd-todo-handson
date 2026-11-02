"""本番ロジック（外部I/Oなし＝純粋ロジック＝評価レイヤーは unit）。"""


class TodoList:
    def __init__(self):
        self._items = []  # [{"title": str, "done": bool}, ...]

    def add(self, title):
        self._items.append({"title": title, "done": False})

    def titles(self):
        return [i["title"] for i in self._items]

    def complete(self, title):
        for i in self._items:
            if i["title"] == title:
                i["done"] = True

    def pending_count(self):
        return len([i for i in self._items if not i["done"]])
