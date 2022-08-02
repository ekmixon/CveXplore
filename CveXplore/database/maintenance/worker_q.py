from queue import Empty, Queue

from .db_action import DatabaseAction


class WorkerQueue(Queue):
    def __init__(self, name, maxsize=0):

        super().__init__(maxsize)
        self.name = name
        self.maxsize = maxsize

        self.closed = False

    def __len__(self):
        self.qsize()

    def __repr__(self):
        return f"<< WorkerQueue:{self.name} >>"

    def __iter__(self):
        return self

    def __next__(self):
        try:
            item = self.get(timeout=1)
            if item is None:
                raise StopIteration
            if isinstance(item, DatabaseAction):
                item = item.entry
            return item
        except Empty:
            raise StopIteration

    def getall(self):
        return list(iter(self))

    def clear(self):
        with self.not_empty:
            self.queue.clear()
            self.not_full.notify()
