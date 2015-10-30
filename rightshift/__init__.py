from copy import copy

__author__ = 'adam.jorgensen.za@gmail.com'


class RightShiftException(BaseException):
    """
    The base class for all exceptions thrown by code in the rightshift library
    """
    pass


class TransformationException(RightShiftException):
    """
    An exception that is raised when a Transform is unable to transform a value
    to another value.
    """
    pass


class ChainTransformer(object):
    """
    The ChainTransformer class is handled specially by the implementation of the
    right shift >> operation in the Transformer class.

    Performing a >> against a ChainTransformer instance causes that instance to
    be called immediately with the left-hand side of the expression. The result
    of this call is used as the return value for the >> operation.

    Overriding this class and implementing the __call__ method allows for the >>
    operator to return a custom Chain sub-class instance rather than an instance
    of the standard Chain class.
    """
    def __call__(self, left):
        """
        """
        raise NotImplementedError


class Transformer(object):
    """
    A Transform is an object which can be called with a single input value.

    If the transformation succeeds, a value will be returned. The returned value
    may be None.

    If the transformation fails, a TransformationException will be raised.

    A Transform may be chained together with other Transforms using the >>
    operation. Chaining functions such that Transforms can be chained
    together from left to right in the order they should logically executed on
    the input value.

    Transforms may also be ANDed or ORed with other Transforms. The manner in
    which this behaves depends greatly on the type of Transforms and some types
    may not be compatible with others with regards to AND/OR. In such a case,
    an Exception will be raised if incompatible types are AND/ORed together.
    """

    def __call__(self, value, **flags):
        """
        __call__ is used to implement the transformation process

        :param value:
        :return:
        """
        raise NotImplementedError

    def __rshift__(self, other):
        """
        __rshift__ is used to implement >> chaining of Transformers.
        :param other:
        :return:
        """
        if isinstance(other, ChainTransformer):
            return other(self)

        if not isinstance(other, Transformer):
            other = Value(other)

        return Chain(self, other)

    def __rrshift__(self, other):
        """
        TODO: Document

        :param other:
        :return:
        """
        return Value(other) >> self

    def __or__(self, other):
        """
        TODO: Document
        """
        if not isinstance(other, Transformer):
            other = Value(other)

        transformers = [self]
        if isinstance(other, Detupling):
            transformers.extend(copy(other.transformers))
        else:
            transformers.append(other)
        return Detupling(*transformers)

    def __ror__(self, other):
        """
        TODO: Document

        :param other:
        :return:
        """
        return Value(other) | self

    def __and__(self, other):
        """
        TODO: Document
        """
        if not isinstance(other, Transformer):
            other = Value(other)

        transformers = [self]
        if isinstance(other, Tupling):
            transformers.extend(copy(other.transformers))
        else:
            transformers.append(other)
        return Tupling(False, *transformers)

    def __rand__(self, other):
        """
        TODO: Document

        :param other:
        :return:
        """
        return Value(other) & self


class Chain(Transformer):
    """
    A Chain is a special Transform that is used to implement the >> operation
    on Transforms.

    When two Transforms are chained together using the >> operator the output
    of the >> operator is a new Transform that can be called in order to return
    the result of calling the right operand with the result of calling the left
    operand. I.e. (a >> b)(x) is synonymous with b(a(x))
    """
    def __init__(self, left, right):
        """
        TODO: Document
        """
        self.left = left
        self.right = right

    def __call__(self, value, **flags):
        """
        TODO: Document
        """
        return self.right(self.left(value, **flags), **flags)


class FlagsChain(Chain):
    """
    TODO: Document
    """
    def __init__(self, flags, left):
        """
        TODO: Document
        """
        super(FlagsChain, self).__init__(left, None)
        self.flags = flags

    def __call__(self, value, **flags):
        """
        TODO: Document
        """
        use_flags = copy(self.flags)
        use_flags.update(flags)
        return self.left(value, **use_flags)


class Flags(ChainTransformer):
    """
    Flags are a special Transform that allows for data to be passed down to
    Transform chain in order to signal Transforms to modify their behaviour.

    Flags are supported in this by the Chain Transform which is aware of Flags
    and handles them in a special fashion to ensure that the Flag information
    is passed on while the Flag object itself is not called as it does not
    implement __call__
    """
    def __init__(self, **flags):
        """
        TODO: Document
        """
        self.flags = flags

    def __call__(self, left):
        return FlagsChain(self.flags, left)

flags = Flags
"""
TODO: Document
"""


class DefaultChain(Chain):
    """
    TODO: Document
    """
    def __init__(self, default, left):
        """
        TODO: Document

        :param default:
        :param left:
        :return:
        """
        super(DefaultChain, self).__init__(left, None)
        self.default = default

    def __call__(self, value, **flags):
        """
        TODO: Document
        """
        try:
            return self.left(value, **flags)
        except TransformationException:
            return self.default


class Default(ChainTransformer):
    """
    TODO: Document
    """
    def __init__(self, default):
        """
        TODO: Document
        """
        self.default = default

    def __call__(self, left):
        return DefaultChain(self.default, left)

default = Default
"""
TODO: Document
"""


class Detupling(Transformer):
    """
    TODO: Document
    """
    def __init__(self, *transformers):
        """
        TODO: Document

        :param transformers:
        :return:
        """
        self.transformers = transformers

    def __call__(self, value, **flags):
        """
        TODO: Document
        """
        for transformer in self.transformers:
            try:
                return transformer(value, **flags)
            except TransformationException:
                pass
        raise TransformationException('Failed to detuple {}'.format(value))

    def __or__(self, other):
        """
        TODO: Document
        """
        if isinstance(other, Transformer):
            transformers = list(copy(self.transformers))
            if isinstance(other, Detupling):
                transformers.extend(other.transformers)
            else:
                transformers.append(other)
            return Detupling(*transformers)
        return super(Detupling, self).__or__(other)

detupling = Detupling
"""
TODO: Document
"""


class Tupling(Transformer):
    """
    TODO: Document
    """
    def __init__(self, generator=False, *transformers):
        """
        TODO: Document
        """
        self.transformers = transformers
        self.generator = generator

    def __call__(self, value, **flags):
        """
        TODO: Document
        """
        if flags.get('tupling__generator', self.generator):
            return (
                transformer(value, **flags)
                for transformer in self.transformers
            )
        else:
            return [
                transformer(value, **flags)
                for transformer in self.transformers
            ]

    def __and__(self, other):
        """
        TODO: Document
        """
        if isinstance(other, Transformer):
            transformers = list(copy(self.transformers))
            if isinstance(other, Tupling):
                transformers.extend(other.transformers)
            else:
                transformers.append(other)
            return Tupling(False, *transformers)
        return super(Tupling, self).__and__(other)


def tupling(*transformers):
    """
    TODO: Document

    :param transformers:
    :return:
    :rtype: Tupling
    """
    return Tupling(False, *transformers)


def lazy_tupling(*transformers):
    """
    TODO: Document

    :param transformers:
    :return:
    :rtype: Tupling
    """
    return Tupling(True, *transformers)


class Value(Transformer):
    """
    Value is a simple Transform that, when called, will simply return the
    value it was instantiated with. Value is used to implement inter-operability
    between Transforms and non-Transform instances.
    """
    def __init__(self, value):
        """
        TODO: Document
        """
        self.value = value

    def __call__(self, value, **flags):
        """
        TODO: Document
        """
        return self.value

value = Value
"""
TODO: Document
"""


class Identity(Transformer):
    """
    Identity is extremely simple and simply returns whatever value it is called with.
    """
    def __call__(self, value, **flags):
        """
        TODO: Document
        """
        return value

identity = Identity()
"""
TODO: Document
"""
