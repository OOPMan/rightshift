from rightshift.extractors import Extractor, ExtractorException
from rightshift.extractors import item


head = item[0]
"""
head is an alias for rightshift.extractors.item[0]
"""


class TailExtractor(Extractor):
    def __call__(self, value, **flags):
        if len(value):
            return value[1:]
        raise ExtractorException('Attempted to obtain tail of empty collection')
tail = TrailExtractor = TailExtractor()
"""
tail is a reference to an instance of rightshift.collections.TailExtractor
"""

last = item[-1]
"""
last is an alias for rightshift.extractors.item[-1]
"""


def take(n):
    """
    take is a shortcut for item[0:n]

    :param n:
    :return:
    """
    return item[0:n]


def take_right(n):
    """
    take_right is a shortcut for item[-n:]

    :param n:
    :return:
    """
    return item[-n:]


class TakeWhileExtractor(Extractor):
    """
    A TakeWhileExtractor instance expects to be called with a value that is
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

take_while = TakeWhileExtractor
"""
take_while is an alias to the TakeWhileExtractor class
"""


def drop(n):
    """
    drop is a short-cut for item[n:]
    :param n:
    :return:
    """
    return item[n:]


def drop_right(n):
    """
    drop_right is a short-cut for item[:-n]
    :param n:
    :return:
    """
    return item[:-n]


class DropWhileExtractor(Extractor):
    """
    A DropWhileExtractor instance expects to be called with a value that is
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
        if flags.get('take_while__generator'):
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

drop_while = DropWhileExtractor
"""
drop_while is an alias to the DropWhileExtractor class
"""


class PartitionExtractor(Extractor):
    """
    A PartitionExtractor instance expects to be called with a value that is
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

partition = PartitionExtractor
"""
partition is an alias to the PartitionExtractor class
"""
