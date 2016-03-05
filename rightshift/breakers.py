from rightshift import Transformer, TransformationException
from rightshift.matchers import Matcher

__author__ = 'adam.jorgensen.za@gmail.com'


class BreakerException(TransformationException): pass


class Breaker(Transformer):
    """
    Breaker is a base class for all Breakers.
    """
    pass


class BreakIf(Breaker):
    """
    A basic Breaker that causes a BreakerException to be thrown if the value
    it is called with does not produced a truthy result when applied to the
    Transformer supplied when the BreakIf instance was created.
    """
    def __init__(self, transformer):
        """

        :param transformer:
        :return:
        """
        if not isinstance(transformer, Transformer):
            raise BreakerException('{} is not an instance of {}'.format(transformer, Transformer.__class__))
        self.transformer = transformer

    def __call__(self, value, **flags):
        """
        :param value:
        :param flags:
        :return:
        """
        if self.transformer(value, **flags):
            raise BreakerException
        return value

break_if = BreakIf
"""
break_if is an alias to the BreakIf class.
"""


class BreakIfNot(BreakIf):
    """
    An inverted version of the BreakIf breaker.
    """

    def __call__(self, value, **flags):
        """

        :param value:
        :param flags:
        :return:
        """
        if not self.transformer(value, **flags):
            raise BreakerException
        return value

break_if_not = BreakIfNot
"""
break_if_not is an alias to the BreakIfNot class.
"""

