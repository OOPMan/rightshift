from builtins import map
from itertools import chain

from future.utils import raise_from

from rightshift import Wrap as _Wrap, TransformationException
from rightshift.extractors import Extractor, ExtractorException
from rightshift.extractors import Item


class Wrap(_Wrap):
    """
    ExtractorException layer over the Wrap transformer
    """
    def __call__(self, value, **flags):
        try:
            return super(Wrap, self).__call__(value, **flags)
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


class TakeWhile(Extractor):
    """
    A TakeWhile instance expects to be called with a value that is
    iterable. When called with such a value it will yield an output iterable
    of all the values that evaluate to truthy when the callable the instance
    was initialised with is called on it up till the point at which a value
    fails the truthiness check.
    """
    def __init__(self, f):
        """
        :param f: A callable object with the signature f(value, **flags)
        """
        if not callable(f):
            raise ExtractorException('{} is not callable'.format(f))
        self.f = f

    def __call__(self, value, **flags):
        if flags.get('take_while__generator'):
            for v in value:
                if self.f(v, **flags):
                    yield v
                else:
                    break
        else:
            output = []
            for v in value:
                if self.f(v, **flags):
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


class DropWhile(Extractor):
    """
    A DropWhile instance expects to be called with a value that is
    iterable. When called with such a value it will yield an output iterable
    omitting all the values that evaluate to truthy when the callable the
    instance was initialised with is called on it up till the point at which a
    value fails the truthiness check.
    """
    def __init__(self, f):
        """
        :param f: A callable object with the signature f(value, **flags)
        """
        if not callable(f):
            raise ExtractorException('{} is not callable'.format(f))
        self.f = f

    def __call__(self, value, **flags):
        if flags.get('drop_while__generator'):
            done = False
            for v in value:
                if not self.f(v, **flags):
                    done = True
                if done:
                    yield v
        else:
            for idx, v in enumerate(value):
                if not self.f(v, **flags):
                    return value[idx:]
            return []

drop_while = DropWhile
"""
drop_while is an alias to the DropWhile class
"""


class Partition(Extractor):
    """
    A Partition instance expects to be called with a value that is
    iterable. When called with such a value it will yield a 2-tuple of lists
    of values produced from values in the iterable partitioned based on
    the truthiness or falsiness per value as determined by the callable
    the instance was initialised with.

    In other news, these doc comments are horrific. I really need to improve
    them.
    """
    def __init__(self, f):
        if not callable(f):
            raise ExtractorException('{} is not callable'.format(f))
        self.f = f

    def __call__(self, value, **flags):
        a = []
        b = []
        for v in value:
            if self.f(v, **flags):
                a.append(v)
            else:
                b.append(v)
        return a, b

partition = Partition
"""
partition is an alias to the Partition class
"""


def filter_with(f):
    """
    Implements the Filter operation

    :param f:
    :return:
    """
    class Filter(Wrap):
        pass
    return Filter(lambda value: filter(f, value))

Filter = filter_ = filter_with
"""
An alias to filter_with
"""


def find(f):
    """
    Implements the Find operation

    :param f:
    :return:
    """
    class Find(Wrap):
        pass
    return Find(lambda value: next(v for v in value if f(v)))

Find = find_with = find
"""
An alias to find
"""


class Map(Extractor):
    """
    Implements the Map operation
    """
    def __init__(self, f):
        if not callable(f):
            raise ExtractorException('{} is not callable'.format(f))
        self.f = f

    def __call__(self, value, **flags):
        if flags.get('map__unpack_value'):
            output = map(self.f, *value)
        else:
            output = map(self.f, value)
        if flags.get('map__generator'):
            return output
        else:
            return list(output)

map_with = map_ = Map


class FlatMap(Extractor):
    """
    Implements the Map and Flatten operation
    """
    def __init__(self, f):
        if not callable(f):
            raise ExtractorException('{} is not callable'.format(f))
        self.f = f

    def __call__(self, value, **flags):
        if flags.get('flat_map__generator'):
            return (v for v in chain.from_iterable(self.f(value)))
        else:
            return [v for v in chain.from_iterable(self.f(value))]

flap_map = FlatMap
