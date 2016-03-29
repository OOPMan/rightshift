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
    by BooleanCondition instances during instantiation or break checking.
    """


class Condition(Transformer):
    """
    """
    def __init__(self, matcher):
        if not isinstance(matcher, Matcher):
            raise ConditionException('matcher parameter must be an instance of '
                                     'rightshift.matchers.Matcher')
        self.matcher = matcher


class BooleanCondition(Condition):
    """
    BooleanCondition is a base class for transformers that use a Matcher
    instance to determine which one of two transformers should be executed and
    its result returned.

    By default the Identity transformer will be executed when the Matcher
    succeeds or fails but this can be changed by calling the .then() and
    .otherwise() methods on the BooleanCondition instance.
    """
    def __init__(self, matcher):
        """
        """
        super(BooleanCondition, self).__init__(matcher)
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


class WhenBooleanCondition(BooleanCondition):
    """
    The WhenBooleanCondition evaluates the matcher and in the event of a True
    result the .then() transformer is called, otherwise the .otherwise()
    transformer is called.
    """
    def __call__(self, value, **flags):
        """
        """
        if self.matcher(value, **flags):
            return self.then_transformer(value, **flags)
        else:
            return self.otherwise_transformer(value, **flags)

when = WhenBooleanCondition
"""
when is an alias to the WhenBooleanCondition within this module.
"""


class WhenNotBooleanCondition(BooleanCondition):
    """
    The WhenNotBooleanCondition evaluates the matcher and in the event of a
    False result the .then() transformer is called, otherwise the .otherwise()
    transform is called.
    """
    def __call__(self, value, **flags):
        if not self.matcher(value, **flags):
            return self.then_transformer(value, **flags)
        else:
            return self.otherwise_transformer(value, **flags)

when_not = WhenNotBooleanCondition
"""
when_not is an alias to the WhenNotBooleanCondition within this module.
"""


class BreakIfCondition(WhenBooleanCondition):
    """
    The BreakIfCondition inherits from the WhenBooleanCondition. When the
    matcher is evaluated and returns True an exception will be raised.
    """
    def __init__(self, matcher):
        super(BreakIfCondition, self).__init__(matcher)
        self.then_transformer = Break

break_if = BreakIfCondition
"""
break_if is an alias to the BreakIfCondition within this module.
"""


class BreakIfNotCondition(WhenNotBooleanCondition, BreakIfCondition):
    """
    The BreakIfNotCondition inherits from the WhenNotBooleanCondition and the
    BreakIfCondition. When the matcher is evaluated and returns False an
    exception will be raised.
    """


break_if_not = BreakIfNotCondition
"""
break_if_not is an alias to BreakIfNotCondition within this module.
"""
