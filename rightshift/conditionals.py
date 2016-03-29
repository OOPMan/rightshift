from rightshift import identity, Transformer, TransformationException
from rightshift.matchers import Matcher

__author__ = 'adam.jorgensen.za@gmail.com'


class BreakException(TransformationException):
    """
    BreakException is raised by the Break transformer when it is called.
    """


class Break(Transformer):
    """
    Break is a simple Transformer that raises a BreakException when it is
    called.
    """
    def __call__(self, value, **kwargs):
        raise BreakException


brk = Break = Break()
"""
brk and Break reference an instance of the rightshift.conditionals.Break class.
"""


class ConditionException(TransformationException):
    """
    ConditionException is a base class for all exceptions that may be thrown
    by Condition instances during instantiation or break checking.
    """


class Condition(Transformer):
    """
    Condition is the base class for transformers that
    """
    def __init__(self, matcher):
        """
        """
        if not isinstance(matcher, Matcher):
            raise ConditionException('matcher parameter must be an instance of '
                                     'rightshift.matchers.Matcher')
        self.matcher = matcher
        self.then_transformer = identity
        self.otherwise_transformer = identity

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

when = WhenCondition
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

when_not = WhenNotCondition
"""
"""


class BreakIfCondition(WhenCondition):
    """
    """
    def __init__(self, matcher):
        super(BreakIfCondition, self).__init__(matcher)
        self.then_transformer = Break

break_if = BreakIfCondition
"""
"""


class BreakIfNotCondition(WhenNotCondition, BreakIfCondition):
    """
    """


break_if_not = BreakIfNotCondition
"""
"""
