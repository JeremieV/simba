from collections.abc import Sequence
from simba.exceptions import IllegalStateException, SimbaException
from simba.lang.Interfaces import ISeq
from simba.lang.types import PersistentMap

# todo: implement hashing

class PersistentList:
    def __init__(self, first, rest = None, count = 1, meta = None):
        self._first = first
        self._rest = rest
        self._count = count
        self.meta = PersistentMap.create() if meta is None else meta

    def first(self):
        return self._first
    def next(self):
        if self._count == 1:
            return None
        return self._rest
    def peek(self):
        return self._first
    def pop(self):
        if self._rest == None:
            return self.empty.withMeta(self.meta)
        return self._rest
    def count(self) -> int:
        return self._count
    def cons(self, o):
        return PersistentList(o, self, self._count + 1, self.meta)
    def empty(self):
        return self.empty.withMeta(self.meta)
    def withMeta(self, meta):
        return PersistentList(self._first, self._rest, self._count, self.meta)
    def __len__(self):
        return self._count
    def __repr__(self) -> str:
        return f"#SimbaPersistentList({' '.join(str(e) for e in self)})"
    def __getitem__(self, sub):
        if isinstance(sub, slice):
            if sub.start is not None and sub.stop is None and (sub.step is None or sub.step == 1):
                # drop the first few elements
                if sub.start < 0:
                    raise IndexError("PersistentList index out of range.")
                head = self
                i = sub.start
                while i > 0:
                    head = head.next()
                    i -= 1
                return head if head is not None else PersistentList.create()
            
            return PersistentList.create(*tuple(self)[sub])
        else:
            if sub < 0:
                sub = self._count + sub
                if sub < 0:
                    raise IndexError("PersistentList index out of range.")
            if not sub < self._count:
                raise IndexError("PersistentList index out of range.")
            if sub == 0:
                return self.first()
            else:
                return self.next()[sub - 1]
    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, PersistentList) or (l := len(self)) != len(__o):
            return False
        for i in range(l):
            if self[i] != __o[i]:
                return False
        return True
    def __add__(self, __o):
        if not isinstance(__o, PersistentList):
            raise SimbaException("Second argument has to be of type PersistentList")
        ret = __o
        for e in self:
            ret = __o.cons(e)
        return ret

class EmptyList(PersistentList, ISeq):
    def __init__(self, meta):
        self.meta = meta
        self._count = 0
    def first(self):
        return None
    def next(self):
        return None
    def cons(self, o):
        return PersistentList(o, None, 1, self.meta)
    def empty(self):
        return self
    def more(self):
        return self
    def peek(self):
        return None
    def pop(self):
        raise IllegalStateException("Can't pop an empty list.")
    def count(self):
        return 0
    def seq(self):
        return None
    def withMeta(m):
        return EmptyList(m)
    def __len__(self) -> int:
        return 0

empty = EmptyList(PersistentMap.create())
PersistentList.empty = empty

# @staticmethod
def creator(*elems):
    ret = empty
    for e in reversed(elems):
        ret = ret.cons(e)
    return ret

PersistentList.create = creator

# tests
# p = PersistentList.create
# assert [*p(1, 2, 3)] == [*(1, 2, 3)]
# assert [p(1, 2, 3)[0]] == [(1, 2, 3)[0]]
# assert [p(1, 2, 3)[2]] == [(1, 2, 3)[2]]
# assert [*p(1, 2, 3)[2:2]] == [*(1, 2, 3)[2:2]]
# assert [*p(1, 2, 3)[0:2]] == [*(1, 2, 3)[0:2]]
# assert [*p(1, 2, 3)[-1:6]] == [*(1, 2, 3)[-1:6]]
# assert [*reversed(p(1, 2, 3, 4, 5, 6))] == [*reversed((1, 2, 3, 4, 5, 6))]