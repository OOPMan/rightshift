from builtins import map
from functools import partial as _partial
from itertools import chain

from future.utils import raise_from

from rightshift import Wrap, TransformationException
from rightshift.extractors import Extractor, ExtractorException
from rightshift.extractors import Item


class WrappedExtractor(Wrap, Extractor):
    """
    ExtractorException layer over the WrappedExtractor transformer
    """
    def __call__(self, value, **flags):
        try:
            return super(WrappedExtractor, self).__call__(value, **flags)
        except TransformationException as e:
            raise_from(ExtractorException, e)


class Head(Item):
    pass

head = Head = Head[0]
"""
head is a reference to an instance of rightshift.collections.Head
"""


class Tail(Extractor):
    def __call__(self, value, **flags):
        if len(value):
            return value[1:]
        raise ExtractorException('Attempted to obtain tail of empty collection')
tail = Tail = Tail()
"""
tail is a reference to an instance of rightshift.collections.Tail
"""


class Last(Item):
    pass

last = Last = Last[-1]
"""
last is an alias for rightshift.extractors.item[-1]
"""


def take(n):
    """
    take is a shortcut for item[0:n]

    :param n:
    :return:
    """
    class Take(Item):
        pass
    return Take[0:n]

Take = take
"""
An alias to take
"""


def take_right(n):
    """
    take_right is a shortcut for item[-n:]

    :param n:
    :return:
    """
    class TakeRight(Item):
        pass
    return TakeRight[-n:]

TakeRight = take_right
"""
An alias to take_right
"""


class TakeWhile(WrappedExtractor):
    """
    A TakeWhile instance expects to be called with a value that is
    iterable. When called with such a value it will yield an output iterable
    of all the values that evaluate to truthy when the callable the instance
    was initialised with is called on it up till the point at which a value
    fails the truthiness check.
    """

    def __init__(self, callable_object, accepts_flags=False, lazy=False):
        super(TakeWhile, self).__init__(callable_object, accepts_flags)
        self.lazy = lazy

    def __call__(self, value, **flags):
        if flags.get('take_while__lazy', self.lazy):
            for v in value:
                if super(TakeWhile, self).__call__(value, **flags):
                    yield v
                else:
                    break
        else:
            output = []
            for v in value:
                if super(TakeWhile, self).__call__(value, **flags):
                    output.append(v)
                else:
                    break
            return output


take_while = TakeWhile
"""
take_while is an alias to the TakeWhile class
"""


def drop(n):
    """
    drop is a short-cut for item[n:]
    :param n:
    :return:
    """
    class Drop(Item):
        pass
    return Drop[n:]

Drop = drop
"""
An alias to drop
"""


def drop_right(n):
    """
    drop_right is a short-cut for item[:-n]
    :param n:
    :return:
    """
    class DropRight(Item):
        pass
    return DropRight[:-n]

DropRight = drop_right
"""
An alias to drop_right
"""


class DropWhile(WrappedExtractor):
    """
    A DropWhile instance expects to be called with a value that is
    iterable. When called with such a value it will yield an output iterable
    omitting all the values that evaluate to truthy when the callable the
    instance was initialised with is called on it up till the point at which a
    value fails the truthiness check.
    """

    def __init__(self, callable_object, accepts_flags=False, lazy=False):
        super().__init__(callable_object, accepts_flags)
        self.lazy = lazy

    def __call__(self, value, **flags):
        if flags.get('drop_while__lazy', self.lazy):
            done = False
            for v in value:
                if not done and not super(DropWhile, self).__call__(v, **flags):
                    done = True
                if done:
                    yield v
        else:
            for idx, v in enumerate(value):
                if not super(DropWhile, self).__call__(v, **flags):
                    return value[idx:]
            return []

drop_while = DropWhile
"""
drop_while is an alias to the DropWhile class
"""


class Partition(WrappedExtractor):
    """
    A Partition instance expects to be called with a value that is
    iterable. When called with such a value it will yield a 2-tuple of lists
    of values produced from values in the iterable partitioned based on
    the truthiness or falsiness per value as determined by the callable
    the instance was initialised with.

    In other news, these doc comments are horrific. I really need to improve
    them.
    """
    def __call__(self, value, **flags):
        a = []
        b = []
        for v in value:
            if super(Partition, self).__call__(v, **flags):
                a.append(v)
            else:
                b.append(v)
        return a, b

partition = Partition
"""
partition is an alias to the Partition class
"""


class Filter(WrappedExtractor):
    """
    Implements the Filter operation
    """
    def __init__(self, callable_object, accepts_flags=False, lazy=False):
        super(Filter, self).__init__(callable_object, accepts_flags)
        self.lazy = lazy

    def __call__(self, value, **flags):
        f = _partial(super(Filter, self).__call__, **flags)
        output = filter(f, value)
        if flags.get('filter__lazy', self.lazy):
            return output
        else:
            return list(output)


filter_with = filter_ = Filter
"""
An alias to filter_with
"""


def find(f):
    """
    Implements the Find operation

    :param f:
    :return:
    """
    class Find(WrappedExtractor):
        pass
    return Find(lambda value: next(v for v in value if f(v)))

Find = find_with = find
"""
An alias to find
"""


class Map(WrappedExtractor):
    """
    Implements the Map operation
    """

    def __init__(self, callable_object, accepts_flags=False, unpack_value=False,
                 lazy=True):
        super().__init__(callable_object, accepts_flags)
        self.unpack_value = unpack_value
        self.lazy = lazy

    def __call__(self, value, **flags):
        from functools import partial
        f = partial(super(Map, self).__call__, **flags)
        if flags.get('map__unpack_value', self.unpack_value):
            output = map(f, *value)
        else:
            output = map(f, value)
        if flags.get('map__lazy', self.lazy):
            return output
        else:
            return list(output)

map_with = map_ = Map


class Flatten(Extractor):
    """
    Implements the Flatten operation
    """

    def __init__(self, lazy=False):
        self.lazy = lazy

    def __call__(self, value, **flags):
        if flags.get('flatten__lazy', self.lazy):
            return (v for v in chain.from_iterable(value))
        else:
            return [v for v in chain.from_iterable(value)]

flatten = Flatten()
lazy_flatten = Flatten(lazy=True)
