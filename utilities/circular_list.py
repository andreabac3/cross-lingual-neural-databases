from typing import *


class CircularList:
    def __init__(self, list_of_node: List[Any]):
        self._list_of_node: List[Any] = list_of_node
        self._index: int = 0
        self._max_length: int = len(list_of_node)

    def add_element(self, element: Any) -> None:
        self._list_of_node.append(element)
        self._max_length += 1

    def get_next(self) -> Any:
        if self._index == self._max_length:
            self._index = 0
        result: Any = self._list_of_node[self._index]
        self._index += 1
        return result

    def get_prev(self):
        self._index -= 1
        if self._index <= 0:
            self._index = self._max_length - 1
        return self._list_of_node[self._index]
