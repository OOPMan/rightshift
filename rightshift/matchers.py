from copy import copy
from future.utils import raise_from
import re

from rightshift import Transformer, RightShiftException
from rightshift.extractors import Item as _Item
from rightshift.extractors import ItemChain as _ItemChain
from rightshift.extractors import Attribute as _Attribute
from rightshift.extractors import AttributeChain as _AttributeChain

__author__ = 'adam.jorgensen.za@gmail.com'


class MatcherException(RightShiftException):
    """
    MatcherException is a base class for all exceptions that may be thrown
    by Matcher instances due either instantiation or matching.
    """
    pass


class Matcher(Transformer):
    """
    Matcher is the base class for all matcher-type transformers. The primary
    function of this class is to extend the __or__ and __and__ methods on
    Transformer in order to enable boolean logic when using the | or &
    with operands which are both sub-classes of the Matcher base class.
    """
    def __or__(self, other):
        """
        When a Matcher instance applies the | operation to another Matcher
        instance the standard Transformer behaviour is overridden.

        A Should instance encapsulating both self and other will be
        returned. If other is an instance of Should then the matchers
        encapsulated within other will be flattened into the new Should
        instance.
        """
        if isinstance(other, Matcher):
            matchers = [self]
            if isinstance(other, Should):
                matchers.extend(copy(other.matchers))
            else:
                matchers.append(other)
            return Should(matchers)

        return super(Matcher, self).__or__(other)

    def __and__(self, other):
        """
        When a Matcher instance applies the & operation to another Matcher
        instance the standard Transformer behaviour is overridden.

        A Must instance encapsulating both self and other will be returned. If
        other is an instance of Must then the matchers encapsulated within other
        will be flattened into the new Must instance.
        """
        if isinstance(other, Matcher):
            matchers = [self]
            if isinstance(other, Must):
                matchers.extend(copy(other.matchers))
            else:
                matchers.append(other)
            return Must(matchers)

        return super(Matcher, self).__and__(other)


class Must(Matcher):
    """
    The Must matcher expects to be initialised with 1 or more Matcher instances.

    When called with a value, the Must matcher returns either True or False.

    True indicates the value matches all Matcher instances the Must was
    initialised with.

    False indicates the value failed to match at least one of the Matcher
    instances that the Must was initialised with. When processing a value,
    False is returned as soon as a failure is detected.
    """
    def __init__(self, matchers):
        """
        TODO: Document
        """
        self.matchers = matchers

    def __call__(self, value, **flags):
        """
        TODO: Document
        """
        for transformer in self.matchers:
            if transformer(value, **flags) is False:
                return False
        return True


def must(*matchers):
    """
    must is a short-cut function for working with the Must class.
    Whereas the Must class constructor expects a single argument which
    is an iterable, this function accepts an arbitrary arguments list which
    is used to construct the Must instance.

    :param matchers:
    :return: A Must instance
    :rtype: Must
    """
    if not matchers:
        raise MatcherException('At least argument must be supplied to '
                               'rightshift.matchers.must')
    return Must(*matchers)


class Should(Matcher):
    """
    The Should matcher expects to be initialised with 1 or more Matcher instances.

    When called with a value, the Should matcher returns either True or False.

    True indicates the value matches one of the Matcher instances the Should was
    initialised with.  When processing a value, True is returned as soon as a
    success is detected.

    False indicates the value failed to match any of the Matcher instances that
    the Should was initialised with.
    """
    def __init__(self, matchers):
        """
        TODO: Document
        """
        self.matchers = matchers

    def __call__(self, value, **flags):
        """
        TODO: Document
        """
        for transformer in self.matchers:
            if transformer(value, **flags) is True:
                return True
        return False


def should(*matchers):
    """
    should is a short-cut function for working with the Should class.
    Whereas the Should class constructor expects a single argument which
    is an iterable, this function accepts an arbitrary arguments list which
    is used to construct the Should instance.

    :param matchers:
    :return: A Should instance
    :rtype: Should
    """
    if not matchers:
        raise MatcherException('At least argument should be supplied to '
                               'rightshift.matchers.should')
    return Should(*matchers)


class MustNot(Matcher):
    """
    The MustNot matcher expects to be initialised with 1 or more Matcher instances.

    When called with a value, the MustNot matcher returns either True or False.

    True indicates the value matches none of the Matcher instances the MustNot
    was initialised with.

    False indicates the value matched one of the Matcher instances that the
    MustNot was initialised with. When processing a value, False is returned as
    soon as a success is detected.
    """
    def __init__(self, matchers):
        """
        TODO: Document
        """
        self.matchers = matchers

    def __call__(self, value, **flags):
        """
        TODO: Document
        """
        for matcher in self.matchers:
            if matcher(value, **flags) is True:
                return False
        return True


def must_not(*matchers):
    """
    must_not is a short-cut function for working with the MustNot class.
    Whereas the MustNot class constructor expects a single argument which
    is an iterable, this function accepts an arbitrary arguments list which
    is used to construct the MustNot instance.

    :param matchers:
    :return: A MustNot instance
    :rtype: MustNot
    """
    if not matchers:
        raise MatcherException('At least argument must_not be supplied to '
                               'rightshift.matchers.must_not')
    return MustNot(*matchers)


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
    A Comparison is a Matcher that should be instantiated with a callable
    object.

    When the Comparison instance is called it will in turn call the comparator
    it was instantiated with in order to obtain a boolean result indicating
    the result of the comparison.

    Additionally, Comparison can be instructed to convert Exceptions during the
    call to the comparator into False results. This can be done either at
    instantiation using the falsey_exceptions parameter or at call time using
    the comparison__falsey_exceptions flag.

    Comparison is sub-classed in order to implement the included LessThan,
    LessThanEqualTo, EqualTo, NotEqualTo, GreaterThanEqualTo and GreaterThan
    matchers.
    """
    def __init__(self, comparator, falsey_exceptions=False):
        """
        :param comparator: A callable object with the signature f(value, **flags)
        :param falsey_exceptions: A boolean value indicating whether exceptions
                                  during comparison should be converted to False
        """
        if not callable(comparator):
            raise MatcherException('{} is not callable'.format(comparator))
        self.comparator = comparator
        self.falsey_exceptions = falsey_exceptions

    def __call__(self, value, **flags):
        try:
            return bool(self.comparator(value, **flags))
        except Exception as e:
            if flags.get('comparison__falsey_exceptions', self.falsey_exceptions):
                return False
            raise_from(MatcherException, e)
        raise NotImplementedError

compare_using = comparison = Comparison
"""
An alias to the Comparison class.

Examples:

compare_using(lambda v, **flags: v.startswith('x'))
"""


class MethodComparison(Comparison):
    """
    TODO: Document
    """
    def __init__(self, value, falsey_exceptions=False):
        """
        TODO: Document

        :param value:
        :param falsey_exceptions:
        :return:
        """
        super(MethodComparison, self).__init__(self.__compare, falsey_exceptions)
        self.value = value

    def __compare(self, value, **flags):
        """
        TODO: Document

        :param value:
        :param flags:
        :return:
        """
        raise NotImplementedError


class LessThan(MethodComparison):
    """
    A Less Than comparison.
    """
    def __compare(self, value, **flags):
        """
        TODO: Document
        """
        return value < self.value

lt = less_than = LessThan
"""
An alias to the LessThan class.
"""


class LessThanEqualTo(MethodComparison):
    """
    A Less than or equal to comparison.
    """
    def __compare(self, value, **flags):
        """
        TODO: Document
        """
        return value <= self.value

lte = less_than_equal_to = LessThanEqualTo
"""
An alias to the LessThanEqualTo class.
"""


class EqualTo(MethodComparison):
    """
    An equal to comparison.
    """
    def __compare(self, value, **flags):
        """
        TODO: Document
        """
        return value == self.value

eq = equal_to = EqualTo
"""
An alias to the EqualTo class.
"""


class NotEqualTo(MethodComparison):
    """
    A not equal to comparison.
    """
    def __compare(self, value, **flags):
        """
        TODO: Document
        """
        return value != self.value

ne = not_equal_to = NotEqualTo
"""
An alias to the NotEqualTo class.
"""


class GreaterThanEqualTo(MethodComparison):
    """
    A greater than or equal to comparison.
    """
    def __compare(self, value, **flags):
        """
        TODO: Document
        """
        return value >= self.value

gte = greater_than_equal_to = GreaterThanEqualTo
"""
An alias to the GreaterThanEqualTo class.
"""


class GreaterThan(MethodComparison):
    """
    A greater than comparison.
    """
    def __compare(self, value, **flags):
        """
        TODO: Document
        """
        return value > self.value

gt = greater_than = GreaterThan
"""
An alias to the GreaterThan class.
"""


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
value_is is a special shortcut to enable working with the Comparison sub-classes
LessThan, LessThanEqualTo, EqualTo, NotEqualTo, GreaterThanEqualTo or GreaterThan
classes to feel more natural.

value is an instance of the private __ValueIs() class. This classes implements
the various comparison operator methods and in order to return instances of the
Comparison sub-classes.

Examples:

value_is >= 5 is equivalent to GreaterThanEqualTo(5)
value_is != True is equivalent to NotEqualTo(True)
"""


class Between(Comparison):
    """
    A between comparison
    """
    def __init__(self, lower_bound, upper_bound, falsey_exceptions=False):
        """
        :param lower_bound: Exclusive lower boundary of the between comparison.
        :param upper_bound: Exclusive upper boundary of the between comparison.
        :param falsey_exceptions: Defaults to False.
        """
        super(Between, self).__init__(self.__compare, falsey_exceptions)
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound

    def __compare(self, value, **flags):
        return self.lower_bound < value < self.upper_bound

btw = between = Between
"""
An alias to the Between class.
"""


class Pattern(Comparison):
    """
    A regex search/match. By default, search is used rather than match.
    """
    def __init__(self, pattern, search=True, falsey_exceptions=False):
        super(Pattern, self).__init__(self.__compare, falsey_exceptions)
        from past.builtins import basestring
        if isinstance(pattern, basestring):
            pattern = re.compile(pattern)
        self.pattern = pattern
        self.search = search

    def __compare(self, value, **flags):
        method = self.pattern.search if flags.get('pattern__search', self.search) else self.pattern.match
        return method(value)

matches_regex = Pattern
"""
An alias to the Pattern class.
"""
