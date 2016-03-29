from rightshift import Transformer, TransformationException
from rightshift.matchers import Matcher

__author__ = 'adam.jorgensen.za@gmail.com'


class BreakException(TransformationException):
    """
    """


class Break(Transformer):
    """
    """
    def __call__(self, value, **kwargs):
        raise BreakException


brk = Break = Break()
"""
"""


class ConditionException(TransformationException):
    """
    """


class Condition(Transformer):
    """
    """
    def __init__(self, matcher):
        """
        """
        if not isinstance(matcher, Matcher):
            raise ConditionException('matcher parameter must be an instance of '
                                     'rightshift.matchers.Matcher')
        self.matcher = matcher
        self.then_transformer = brk
        self.otherwise_transformer = brk

    def then(self, transformer):
        """
        """
        if not isinstance(transformer, Transformer):
            raise ConditionException('transformer parameter must be an '
                                     'instance of rightshift.Transformer')
        self.then_transformer = transformer
        return self

    def otherwise(self, transformer):
        """
        """
        if not isinstance(transformer, Transformer):
            raise ConditionException('transformer parameter must ben an '
                                     'instance of rightshift.Transformer')
        self.otherwise_transformer = transformer
        return self


class WhenCondition(Condition):
    """
    """
    def __call__(self, value, **flags):
        """
        """
        if self.matcher(value, **flags):
            return self.then_transformer(value, **flags)
        else:
            return self.otherwise_transformer(value, **flags)

when = break_if = WhenCondition
"""
"""


class WhenNotCondition(Condition):
    """
    """
    def __call__(self, value, **flags):
        if not self.matcher(value, **flags):
            return self.then_transformer(value, **flags)
        else:
            return self.otherwise_transformer(value, **flags)

when_not = break_if_not = WhenNotCondition
"""
"""
