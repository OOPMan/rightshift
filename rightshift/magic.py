__author__ = 'adam.jorgensen.za@gmail.com'


class IndexOrAccessToInstantiate(type):
    """
    This metaclass enables a class to be indexed or access in order to
    trigger instantiation of the class.

    For a class that makes use of this metaclass the following usages
    are identical:

    a = ClassX('value')
    a = ClassX.value
    a = ClassX['value']

    In order for this metaclass to function correctly any class that makes use
    of it needs to ensure its __init__ function is correctly defined to handle
    the behaviour demonstrated above.
    """
    def __getattr__(cls, name):
        return cls(name)

    def __getitem__(cls, name):
        return cls(name)
