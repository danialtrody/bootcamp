from typing import Any
import time


class Node:
    def __init__(
        self,
        key: str,
        value: Any,
        timestamp: float,
        prev: Node | None = None,
        next: Node | None = None,
    ) -> None:

        self.key = key
        self.value = value
        self.timestamp = timestamp
        self.prev = prev
        self.next = next


class MyLruCache:
    def __init__(self, maxsize: int, ttl: float) -> None:

        if maxsize <= 0:
            raise ValueError("maxsize must be > 0")

        if ttl <= 0:
            raise ValueError("ttl must be > 0")

        self.maxsize = maxsize
        self.ttl = ttl

        self.cache: dict[str, Node] = {}

        self.head = Node("head", None, 0)
        self.tail = Node("tail", None, 0)

        self.head.next = self.tail
        self.tail.prev = self.head

    def get(self, key: str) -> Any | None:

        if key not in self.cache:
            return None

        node = self.cache[key]

        if self._is_expired(node):
            self._remove_node(node)
            self.cache.pop(key)
            return None

        self._move_to_front(node)

        return node.value

    def set(self, key: str, value: Any) -> None:

        if key in self.cache:
            node = self.cache.get(key)

            if node is not None:
                if self._is_expired(node):
                    self._remove_node(node)
                    self.cache.pop(key, None)
                else:
                    node.value = value
                    node.timestamp = time.time()
                    self._move_to_front(node)
                    return
        new_node = Node(key, value, time.time())
        self.cache[key] = new_node
        self._add_to_front(new_node)

        if len(self.cache) > self.maxsize:
            node_to_remove = self.tail.prev
            if node_to_remove and node_to_remove != self.head:
                self._remove_node(node_to_remove)
                self.cache.pop(node_to_remove.key, None)

    def clear(self) -> None:
        self.cache.clear()

        self.head.next = self.tail
        self.tail.prev = self.head

    def __len__(self) -> int:
        return len(self.cache)

    def __contains__(self, key: str) -> bool:
        if key not in self.cache:
            return False

        node = self.cache[key]

        if self._is_expired(node):
            self._remove_node(node)
            self.cache.pop(key)
            return False

        return True

    def _move_to_front(self, node: Node) -> None:
        self._remove_node(node)
        self._add_to_front(node)

    def _add_to_front(self, node: Node) -> None:

        if node is None or self.head.next is None:
            return

        node.next = self.head.next
        node.prev = self.head

        self.head.next.prev = node
        self.head.next = node

    def _remove_node(self, node: Node) -> None:
        if not node:
            return

        if node.prev:
            node.prev.next = node.next

        if node.next:
            node.next.prev = node.prev

        node.prev = None
        node.next = None

    def _is_expired(self, node: Node) -> bool:
        return time.time() - node.timestamp > self.ttl
