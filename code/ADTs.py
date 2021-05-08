from typing import *


class Queue():

    def __init__(self):
        self.items = []

    def is_empty(self) -> bool:
        return len(self.items) == 0

    def enqueue(self, item: Any) -> None:
        self.items.append(item)

    def dequeue(self) -> Any:
        if self.is_empty():
            raise Exception
        return self.items.pop(0)

    def empty_queue(self) -> None:
        while not self.is_empty():
            self.dequeue()



