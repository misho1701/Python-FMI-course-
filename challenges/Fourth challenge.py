from collections import deque


class Slot:
    def __init__(self, object_limit=None, size_limit=None):
        self.object_limit = object_limit
        self.size_limit = size_limit
        self.name = None

    def __set_name__(self, owner, name):
        self.name = f"_slot_{name}"

    def _get_queue(self, instance):
        if not hasattr(instance, self.name):
            setattr(instance, self.name, deque())
        return getattr(instance, self.name)

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return tuple(self._get_queue(instance))

    def __set__(self, instance, value):
        q = self._get_queue(instance)

        if self.object_limit is not None and len(q) + 1 > self.object_limit:
            raise ValueError("Object limit exceeded")

        if self.size_limit is not None:
            current_size = sum(len(x) for x in q)
            if current_size + len(value) > self.size_limit:
                raise ValueError("Size limit exceeded")

        q.append(value)

    def __delete__(self, instance):
        q = self._get_queue(instance)
        if q:
            q.popleft()

