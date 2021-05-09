import itertools
from heapq import *
from box import Box
from typing import *


class MoreHeapQ:
    """
    An extension of python's heapq module which allows for the action of decreasing priority of an item in the heap.

    ****
    Codsmall ce primarily copied from the python heapq docs here (with a few small changes):
        https://docs.python.org/2/library/heapq.html#priority-queue-implementation-notes
    ***

    Public Attributes
    =================
    pq: the heap
    entry_finder: a mapping of tasks to entries
    REMOVED: a string to represent a removed task/item
    counter: a unique sequence count
    size: how many non-removed items there are in this priority queue
    """
    pq: list
    entry_finder: dict
    REMOVED: str
    counter: itertools.count
    size: int



    def __init__(self):
        self.pq = []                      # list of entries arranged in a heap
        self.entry_finder = {}               # mapping of tasks to entries
        self.REMOVED = '<removed-task>'      # placeholder for a removed task
        self.counter = itertools.count()     # unique sequence count
        self.size = 0

    def add_task(self, task, priority=0):
        'Add a new task or update the priority of an existing task'
        if task in self.entry_finder:
            self.remove_task(task)
        count = next(self.counter)
        entry = [priority, count, task]
        self.entry_finder[task] = entry
        heappush(self.pq, entry)
        self.size += 1

    def remove_task(self, task):
        'Mark an existing task as REMOVED.  Raise KeyError if not found.'
        entry = self.entry_finder.pop(task)
        entry[-1] = self.REMOVED
        self.size -= 1

    def pop_task(self):
        'Remove and return the lowest priority task. Raise KeyError if empty.'
        while self.pq:
            priority, count, task = heappop(self.pq)
            if task is not self.REMOVED:
                del self.entry_finder[task]
                self.size -= 1
                return task
        raise KeyError('pop from an empty priority queue')


if __name__ == "__main__":
    heap = More_HeapQ()
    heap.add_task((1,1), 2)
    heap.add_task((2,2), 5)
    heap.add_task((3,3), 4)
    heap.add_task((4,4), 15)
    heap.add_task((5,5), 7)
    heap.add_task((2,2), 7)

    print(heap.pq)
    heap.remove_task((4,4))
    print(heap.pq)
    heap.pop_task()
    print(heap.pq)
    heap.remove_task((3,3))
    print(heap.pq)
    x = heap.pop_task()
    print("popped of", x)

