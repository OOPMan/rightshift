from copy import copy

from future.utils import raise_from

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
        return self(other)

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
        return Detupling(transformers)

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
        return Tupling(transformers)

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
    operand.

    Examples:

    f = a >> b
    z = f(x)

    is synonymous with

    z = b(a(x))

    Additionally, Chain instances provide an implementation of the << operator.
    Using the << operator allows one to produce a new chain with the right-hand
    operand inserted between the left and right sides of the current chain.

    Examples:

    f = a >> b
    f = f << c

    is equivalent to

    f = a >> b << c
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

    def __lshift__(self, other):
        """
        TODO: Document
        """
        return self.left >> other >> self.right


class Detupling(Transformer):
    """
    TODO: Document
    """
    def __init__(self, transformers):
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
            return Detupling(transformers)
        return super(Detupling, self).__or__(other)


def detupling(*transformers):
    """
    detupling is a short-cut function for working with the Detupling class.
    Whereas the Detupling class constructor expects a single argument which
    is an iterable, this function accepts an arbitrary arguments list which
    is used to construct the Detupling instance.

    :param transformers:
    :return: A Detupling instance
    :rtype: Detupling
    """
    if not transformers:
        raise TransformationException('At least argument must be supplied to '
                                      'rightshift.detupling')
    return Detupling(transformers)


class Tupling(Transformer):
    """
    TODO: Document
    """
    def __init__(self, transformers, generator=False):
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
            return Tupling(transformers, self.generator)
        return super(Tupling, self).__and__(other)


def tupling(*transformers):
    """
    tupling is a short-cut function for working with the Tupling class.
    Whereas the Tupling class constructor expects its first argument to
    be an iterable, this function accepts an arbitrary arguments list which
    is used to construct the Tupling instance.

    :param transformers:
    :return:
    :rtype: Tupling
    """
    if not transformers:
        raise TransformationException('At least argument must be supplied to '
                                      'rightshift.tupling')
    return Tupling(transformers)


def lazy_tupling(*transformers):
    """
    tupling is a short-cut function for working with the Tupling class.
    Whereas the Tupling class constructor expects its first argument to
    be an iterable, this function accepts an arbitrary arguments list which
    is used to construct the Tupling instance. Additionally, this function
    instructs the Tupling instance to use generator logic by default.

    :param transformers:
    :return:
    :rtype: Tupling
    """
    if not transformers:
        raise TransformationException('At least argument must be supplied to '
                                      'rightshift.lazy_tupling')
    return Tupling(transformers, True)


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

value = val = Value
"""
value and val are aliases for the Value transform.
"""


class Identity(Transformer):
    """
    Identity is extremely simple and simply returns whatever value it is called
    with.
    """
    def __call__(self, value, **flags):
        return value

identity = ident = Identity = Identity()
"""
identity and Identity reference an instance of the rightshift.Identity class.
"""


class Wrap(Transformer):
    """
    Wrap allows you to easily re-use an existing callable object in the context
    of a RightShift chain.
    """
    def __init__(self, callable_object):
        if not callable(callable_object):
            raise TransformationException('{} is not callable'.format(callable_object))
        self.callable_object = callable_object

    def __call__(self, value, **flags):
        try:
            return self.callable_object(value)
        except Exception as e:
            raise_from(TransformationException, e)

wrap = Wrap
"""
wrap is an alias for the Wrap transform.
"""
