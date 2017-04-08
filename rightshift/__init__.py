import re
from copy import copy, deepcopy

from future.utils import raise_from, with_metaclass

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


def _underscore(word):
    """
    Shameless nicked from inflection.

    See http://inflection.readthedocs.io/en/latest/#inflection.underscore
    """
    word = re.sub(r"([A-Z]+)([A-Z][a-z])", r'\1_\2', word)
    word = re.sub(r"([a-z\d])([A-Z])", r'\1_\2', word)
    word = word.replace("-", "_")
    return word.lower()


class Flags(dict):
    """
    A tweaked dictionary that allows attribute-style access and 
    enforces a namespace system
    """
    def __init__(self, prefix, mapping=None, **kwargs):
        self.prefix = prefix
        super(Flags, self).__init__(mapping, **kwargs)

    def __getitem__(self, item):
        if not item.startswith(self.prefix):
            return super(Flags, self).__getitem__(self.prefix + item)
        return super(Flags, self).__getitem__(item)

    def __getattr__(self, item):
        return self[item]


# TODO: We can probably relocate the functions on this back into the HasFlags builder now
class HasFlagsBase(type):
    """
    The HasFlagsBase metaclass

    TODO: Document
    """
    @staticmethod
    def __new__(mcs, name, bases, members, prefix=None, flags=None):
        _prefix = _underscore(name) if prefix is None else prefix
        _prefix += '__'
        mcs.prefix = property(lambda cls: _prefix[:-2])

        flags = {} if flags is None else flags
        base_flags = {}
        for base in bases:
            meta = type(base)
            if issubclass(meta, (HasFlagsBase,)):
                base_flags.update(base.default_flags)
        base_flags.update(flags)
        flags = base_flags
        mcs.default_flags = property(lambda _: deepcopy(flags))
        mcs.flags = lambda _, **kwargs: {_prefix + k: v for k, v in kwargs.items()}

        temporary_class = super(HasFlagsBase, mcs).__new__(mcs, name, bases,
                                                           members)
        base__call__ = getattr(temporary_class, '__call__', None)
        if base__call__ is None:
            raise RightShiftException('__call__ must be defined')
        base__call__is_wrapper = getattr(base__call__, '_is_has_flags_wrapper',
                                         False)

        def __call__(self, value, **kwargs):
            """
            Wraps the __call__ function defined on the class being defined
            in order to transform input **kwargs style flag values into 
            an instance of our custom Flags dictionary class. This is used
            to allowed Transformers to be written such that they expect to
            receive flag values in the **kwargs style but pass them on to the
            underlying __call__ as a standard parameter. As such, this function
            is essential a non-signature preserving decorator
            
            :param self: 
            :param value: 
            :param kwargs: 
            :return: 
            """
            prefix = type(self).prefix + '__'
            for flag, flag_value in flags.items():
                key = prefix + flag
                if key not in kwargs:
                    kwargs[key] = getattr(self, flag, flag_value)
            if base__call__is_wrapper:
                return base__call__(self, value, **Flags(prefix, kwargs))
            else:
                return base__call__(self, value, Flags(prefix, kwargs))
        __call__._is_has_flags_wrapper = True
        members['__call__'] = __call__

        # TODO: Add a flags method to the class that can be used to generate
        # flags data for submission to the flags helpfer function

        return super(HasFlagsBase, mcs).__new__(mcs, name, bases, members)


def HasFlags(*bases, prefix=None, **flags):
    """
    Generates a HasFlags metaclass

    TODO: Document

    :param *bases:
    :param prefix:
    :param flags:
    :return:
    """
    meta_bases = tuple(set([
        type(base) for base in bases
        if issubclass(type(base), HasFlagsBase)
    ]))
    meta_bases = (HasFlagsBase,) if not meta_bases else meta_bases

    @staticmethod
    def __new__(mcs, name, bases, members):
        return HasFlagsBase.__new__(mcs, name, bases, members, prefix, flags)

    def __call__(cls, *args, **kwargs):
        """
        TODO: Document

        :param args:
        :param kwargs:
        :return:
        """
        instance_flags = deepcopy(flags)
        for flag in flags:
            if flag in kwargs:
                instance_flags[flag] = kwargs[flag]
                del kwargs[flag]
        instance = HasFlagsBase.__call__(cls, *args, **kwargs)
        for flag, flag_value in instance_flags.items():
            setattr(instance, flag, flag_value)
        return instance
    members = {
        '__new__': __new__,
        '__call__': __call__
    }
    meta = type('HasFlags', meta_bases, members)
    return with_metaclass(meta, *bases)


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


class Transformer(HasFlags(object)):
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

    def __call__(self, value, flags):
        """
        __call__ is used to implement the transformation process

        :param value:
        :param flags:
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
            raise TransformationException('A Transformer may only be chained'
                                          'with another Transformer')

        return Chain(self, other)

    def __rrshift__(self, other):
        """
        TODO: Document

        :param other:
        :return:
        """
        # TODO: This should exclude ChainTransformers
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


class OptionallyLazyTransformer(HasFlags(Transformer, lazy=False)):
    """
    An OptionallyLazyTransformer is one that can optionally return a value with 
    is lazy in nature (E.g. a generator or some other object that implements the 
    iterator protocol)
    
    
    """
    def __lazy_call__(self, value, flags):
        """
        This method implements the lazy form of the transformation
        
        :param value: 
        :param flags: 
        :return: 
        """
        raise NotImplementedError

    def __eager_call__(self, value, flags):
        """
        This method implements the eager form of the transformation. Often this
        is done by simply converting the result of the lazy form to concrete a
        value or values.
        
        :param value: 
        :param flags: 
        :return: 
        """
        raise NotImplementedError

    def __call__(self, value, flags):
        """
        This method implements the determination of whether to invoke the lazy
        or eager form of the transformation
        
        :param value: 
        :param flags: 
        :return: 
        """
        method = self.__lazy_call__ if flags.lazy else self.__eager_call__
        return method(value, flags)


class LazyTransformer(HasFlags(OptionallyLazyTransformer, lazy=True)):
    """
    This class overrides the OptionallyLazyTransformer to make laziness the
    default option. It may be an appropriate base for certain kinds of
    transformers.
    """


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

    def __call__(self, value, flags):
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

    def __call__(self, value, flags):
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
        raise TransformationException('At least one argument must be supplied '
                                      'to rightshift.detupling')
    return Detupling(transformers)


class Tupling(HasFlags(Transformer, lazy=False)):
    """
    TODO: Document
    """
    def __init__(self, transformers):
        """
        TODO: Document
        """
        self.transformers = transformers

    def __call__(self, value, flags):
        """
        TODO: Document
        """
        if flags.lazy:
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
    return Tupling(transformers, lazy=True)


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

    def __call__(self, value, flags):
        """
        TODO: Document
        """
        return self.value

value = val = const = constant = Value
"""
value and val are aliases for the Value transform.
"""


class Identity(Transformer):
    """
    Identity is extremely simple and simply returns whatever value it is called
    with.
    """
    def __call__(self, value, flags):
        return value

identity = ident = Identity = Identity()
"""
ident, identity and Identity reference an instance of the rightshift.Identity
class.
"""


class Wrap(HasFlags(Transformer, accepts_flags=False)):
    """
    Wrap allows you to easily re-use an existing callable object in the context
    of a RightShift chain.
    """
    def __init__(self, callable_object):
        if not callable(callable_object):
            raise TransformationException('{} is not callable'.format(callable_object))
        self.callable_object = callable_object

    def __call__(self, value, flags):
        try:
            if flags.accepts_flags:
                return self.callable_object(value, **flags)
            else:
                return self.callable_object(value)
        except Exception as e:
            raise_from(TransformationException, e)

wrap = Wrap
"""
wrap is an alias for the Wrap transform.
"""
