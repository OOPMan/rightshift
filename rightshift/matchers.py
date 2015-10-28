from copy import copy
from rightshift import Transformer

__author__ = 'adam.jorgensen.za@gmail.com'


class Matcher(Transformer):
    """
    TODO: Document
    """
    def __or__(self, other):
        """
        TODO: Document
        """
        if isinstance(other, Matcher):
            transformers = [self]
            if isinstance(other, BooleanOr):
                transformers.extend(copy(other.transformers))
            else:
                transformers.append(other)
            return BooleanOr(*transformers)

        return super(Matcher, self).__or__(other)

    def __and__(self, other):
        """
        TODO: Document
        """
        if isinstance(other, Matcher):
            transformers = [self]
            if isinstance(other, BooleanAnd):
                transformers.extend(copy(other.transformers))
            else:
                transformers.append(other)
            return BooleanAnd(*transformers)

        return super(Matcher, self).__and__(other)


class BooleanAnd(Matcher):
    """
    TODO: Document
    """
    def __init__(self, *transformers):
        """
        TODO: Document
        """
        self.transformers = transformers

    def __call__(self, value, **flags):
        """
        TODO: Document
        """
        for transformer in self.transformers:
            if transformer(value, **flags) is False:
                return False
        return True


class BooleanOr(Matcher):
    """
    TODO: Document
    """
    def __init__(self, *transformers):
        """
        TODO: Document
        """
        self.transformers = transformers

    def __call__(self, value, **flags):
        """
        TODO: Document
        """
        for transformer in self.transformers:
            if transformer(value, **flags) is True:
                return True
        return False


class InstanceOf(Matcher):
    """
    An InstanceOf matcher is very simple. When called with a value it will indicate
    whether the value is an instance of the type the matcher was instantiated
    with.

    """
    def __init__(self, type):
        """
        :param type: A type or tuple of types.
        """
        self.type = type

    def __call__(self, value, **flags):
        return isinstance(value, self.type)

instance_of = InstanceOf
"""
instance_of is a an alias to the InstanceOf class within this module.
"""

