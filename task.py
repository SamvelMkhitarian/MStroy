from typing import Any


class TreeStore:
    def __init__(self, items: list[dict[str, Any]]):
        """
        Инициализирует объект TreeStore с массивом элементов.
        """
        self.items: list[dict[str, Any]] = items
        self.item_by_id: dict[int, dict[str, Any]] = {
            item['id']: item for item in items}
        self.children_by_parent: dict[int | str, list[dict[str, Any]]] = {}
        for item in items:
            parent = item['parent']
            if parent not in self.children_by_parent:
                self.children_by_parent[parent] = []
            self.children_by_parent[parent].append(item)

    def getAll(self) -> list[dict[str, Any]]:
        """
        Возвращает исходный массив элементов.
        """
        return self.items

    def getItem(self, id: int) -> dict[str, Any] | None:
        """
        Возвращает элемент по его ID.
        """
        return self.item_by_id.get(id)

    def getChildren(self, id: int) -> list[dict[str, Any]]:
        """
        Возвращает дочерние элементы для заданного элемента.
        """
        return self.children_by_parent.get(id, [])

    def getAllParents(self, id: int) -> list[dict[str, Any]]:
        """
        Возвращает всех родительских элементов для заданного элемента, начиная от него до корневого элемента.
        """
        parents = []
        current_item = self.item_by_id.get(id)
        while current_item and current_item['parent'] != 'root':
            parent_id = current_item['parent']
            parent_item = self.item_by_id.get(parent_id)
            if parent_item:
                parents.append(parent_item)
                current_item = parent_item
            else:
                break
        return parents


# Пример использования
items = [
    {"id": 1, "parent": "root"},
    {"id": 2, "parent": 1, "type": "test"},
    {"id": 3, "parent": 1, "type": "test"},
    {"id": 4, "parent": 2, "type": "test"},
    {"id": 5, "parent": 2, "type": "test"},
    {"id": 6, "parent": 2, "type": "test"},
    {"id": 7, "parent": 4, "type": None},
    {"id": 8, "parent": 4, "type": None}
]

ts = TreeStore(items)

# Примеры использования:
print(ts.getAll())  # [{"id":1,"parent":"root"}, {...}, {...}, ...]
print(ts.getItem(7))  # {"id":7,"parent":4,"type":None}
# [{"id":7,"parent":4,"type":None}, {"id":8,"parent":4,"type":None}]
print(ts.getChildren(4))
print(ts.getChildren(5))  # []
# [{"id":4,"parent":2,"type":"test"}, {"id":2,"parent":1,"type":"test"}, {"id":1,"parent":"root"}]
print(ts.getAllParents(7))
