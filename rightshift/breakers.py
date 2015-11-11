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
    it is called with does not match the Matcher supplied when the BreakIf
    instance was created.
    """
    def __init__(self, matcher):
        """

        :param matcher:
        :return:
        """
        if not isinstance(matcher, Matcher):
            raise BreakerException('{} is not an instance of {}'.format(matcher, Matcher.__class__))
        self.matcher = matcher

    def __call__(self, value, **flags):
        """
        :param value:
        :param flags:
        :return:
        """
        if self.matcher(value, **flags):
            raise BreakerException
        return value


break_if = BreakIf
"""
break_if is an alias to the BreakIf class.
"""
