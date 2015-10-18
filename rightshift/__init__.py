__author__ = 'adam.jorgensen.za@gmail.com'


class TransformationException(BaseException):
    """
    An exception that is raised when a Transform is unable to transform a value
    to another value.
    """
    pass


class Transformer(object):
    """
    A Transform is an object which can be called with a single input value.

    If the transformation succeeds, a value will be returned. The returned value
    may be None.

    If the transformation fails, a TransformationException will be raised.
    """

    def __call__(self, value):
        raise NotImplementedError
