from copy import copy
from rightshift import Transformer, RightShiftException

__author__ = 'adam.jorgensen.za@gmail.com'


class MatcherException(RightShiftException):
    """
    TODO: Document
    """
    pass


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

true_for_all_of = all = every = BooleanAnd
"""
TODO: Document
"""


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

true_for_one_of = some = any = BooleanOr
"""
TODO: Document
"""


class IsInstance(Matcher):
    """
    An IsInstance matcher is very simple. When called with a value it will indicate
    whether the value is an instance of the type the matcher was instantiated
    with.

    """
    def __init__(self, type):
        """
        :param type: A type or tuple of types.
        """
        self.type = type

    def __call__(self, value, **flags):
        """
        TODO: Document
        """
        return isinstance(value, self.type)

is_instance = IsInstance
"""
is_instance is a an alias to the IsInstance class within this module.
"""


class Comparison(Matcher):
    """
    TODO: Document
    """
    def __init__(self, value):
        """
        TODO: Document
        """
        self.value = value
        self.type = type(value)


class LessThan(Comparison):
    """
    TODO: Document
    """
    def __call__(self, value, **flags):
        """
        TODO: Document
        """
        return isinstance(value, self.type) and value < self.value


class LessThanEqualTo(Comparison):
    """
    TODO: Document
    """
    def __call__(self, value, **flags):
        """
        TODO: Document
        """
        return isinstance(value, self.type) and value <= self.value


class EqualTo(Comparison):
    """
    TODO: Document
    """
    def __call__(self, value, **flags):
        """
        TODO: Document
        """
        return isinstance(value, self.type) and value == self.value


class NotEqualTo(Comparison):
    """
    TODO: Document
    """
    def __call__(self, value, **flags):
        """
        TODO: Document
        """
        return isinstance(value, self.type) and value != self.value


class GreaterThanEqualTo(Comparison):
    """
    TODO: Document
    """
    def __call__(self, value, **flags):
        """
        TODO: Document
        """
        return isinstance(value, self.type) and value >= self.value


class GreaterThan(Comparison):
    """
    TODO: Document
    """
    def __call__(self, value, **flags):
        """
        TODO: Document
        """
        return isinstance(value, self.type) and value > self.value


class __ValueIs(object):
    """
    TODO: Document
    """
    def __lt__(self, other):
        """
        TODO: Document
        """
        return LessThan(other)

    def __le__(self, other):
        """
        TODO: Document
        """
        return LessThanEqualTo(other)

    def __eq__(self, other):
        """
        TODO: Document
        """
        return EqualTo(other)

    def __ne__(self, other):
        """
        TODO: Document
        """
        return NotEqualTo(other)

    def __ge__(self, other):
        """
        TODO: Document
        """
        return GreaterThanEqualTo(other)

    def __gt__(self, other):
        """
        TODO: Document
        """
        return GreaterThan(other)

value_is = __ValueIs()
"""
TODO: Document
"""


class IsNot(Matcher):
    """
    TODO: Document
    """
    def __init__(self, matcher):
        """
        TODO: Document
        """
        if not isinstance(matcher, Matcher):
            raise MatcherException('{} is not an instance of '
                                   'rightshift.matchers.Matcher'.format(matcher))
        self.matcher = matcher

    def __call__(self, value, **flags):
        """
        TODO: Document
        """
        return not self.matcher(value, **flags)

is_not = IsNot
