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
            if isinstance(other, Should):
                transformers.extend(copy(other.matchers))
            else:
                transformers.append(other)
            return Should(*transformers)

        return super(Matcher, self).__or__(other)

    def __and__(self, other):
        """
        TODO: Document
        """
        if isinstance(other, Matcher):
            transformers = [self]
            if isinstance(other, Must):
                transformers.extend(copy(other.matchers))
            else:
                transformers.append(other)
            return Must(*transformers)

        return super(Matcher, self).__and__(other)


class Must(Matcher):
    """
    TODO: Document
    """
    def __init__(self, *matchers):
        """
        TODO: Document
        """
        if not matchers:
            raise MatcherException('At least one instance of rightshift.matchers'
                                   '.Matcher must be supplied to Must.__init__')
        for matcher in matchers:
            if not isinstance(matcher, Matcher):
                raise MatcherException('{} is not an instance of '
                                       'rightshift.matchers.Matcher'.format(matcher))
        self.matchers = matchers

    def __call__(self, value, **flags):
        """
        TODO: Document
        """
        for transformer in self.matchers:
            if transformer(value, **flags) is False:
                return False
        return True

must = Must
"""
must is an alias to the Must class in righshift.matchers.
"""


class Should(Matcher):
    """
    TODO: Document
    """
    def __init__(self, *matchers):
        """
        TODO: Document
        """
        if not matchers:
            raise MatcherException('At least one instance of rightshift.matchers'
                                   '.Matcher must be supplied to Should.__init__')
        for matcher in matchers:
            if not isinstance(matcher, Matcher):
                raise MatcherException('{} is not an instance of '
                                       'rightshift.matchers.Matcher'.format(matcher))
        self.matchers = matchers

    def __call__(self, value, **flags):
        """
        TODO: Document
        """
        for transformer in self.matchers:
            if transformer(value, **flags) is True:
                return True
        return False

should = Should
"""
should is an alias to the Should class in rightshift.matchers.
"""


class MustNot(Matcher):
    """
    TODO: Document
    """
    def __init__(self, *matchers):
        """
        TODO: Document
        """
        if not matchers:
            raise MatcherException('At least one instance of rightshift.matchers'
                                   '.Matcher must be supplied to MustNot.__init__')
        for matcher in matchers:
            if not isinstance(matcher, Matcher):
                raise MatcherException('{} is not an instance of '
                                       'rightshift.matchers.Matcher'.format(matcher))
        self.matchers = matchers

    def __call__(self, value, **flags):
        """
        TODO: Document
        """
        for matcher in self.matchers:
            if matcher(value, **flags) is True:
                return False
        return True

must_not = MustNot


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
