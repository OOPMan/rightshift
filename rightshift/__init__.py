from copy import copy

__author__ = 'adam.jorgensen.za@gmail.com'


class TransformationException(BaseException):
    """
    An exception that is raised when a Transform is unable to transform a value
    to another value.
    """
    pass


class ChainException(TransformationException):
    """
    An exception that is raised when an attempt to chain two Transforms together
    fails.
    """
    pass


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
        if isinstance(other, Transformer):
            return Chain(self, other)

        raise TypeError('{} is not an instance of Transformer'.format(other))

    def __or__(self, other):
        """
        TODO: Document
        """
        if isinstance(other, Transformer):
            transformers = [self]
            if isinstance(other, Detupling):
                transformers.extend(copy(other.transformers))
            else:
                transformers.append(other)
            return Detupling(*transformers)

        raise TransformationException('Unable to detuple {} with {}'.format(self, other))

    def __and__(self, other):
        """
        TODO: Document
        """
        if isinstance(other, Transformer):
            transformers = [self]
            if isinstance(other, Tupling):
                transformers.extend(copy(other.transformers))
            else:
                transformers.append(other)
            return Tupling(False, *transformers)

        raise TransformationException('Unable to tuple {} with {}'.format(self, other))


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
        self.left = left
        self.right = right

    def __call__(self, value, **flags):
        if isinstance(self.right, Flags):
            use_flags = copy(self.right.flags)
            use_flags.update(flags)
            return self.left(value, **use_flags)
        else:
            return self.right(self.left(value, **flags), **flags)


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

tupling = Tupling


class Flags(Transformer):
    """
    Flags are a special Transform that allows for data to be passed down to
    Transform chain in order to signal Transforms to modify their behaviour.

    Flags are supported in this by the Chain Transform which is aware of Flags
    and handles them in a special fashion to ensure that the Flag information
    is passed on while the Flag object itself is not called as it does not
    implement __call__
    """
    def __init__(self, flags):
        self.flags = flags

flags = Flags

