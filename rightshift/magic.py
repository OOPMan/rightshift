__author__ = 'adam.jorgensen.za@gmail.com'


class IndexOrAccessToInstantiate(type):
    """
    This metaclass enables a class to be indexed or access in order to
    trigger instantiation of the class.

    For a class that makes use of this metaclass the following usages
    are identical:

    ClassX.value == ClassX('value', IndexOrAccessToInstantiate.ATTR)
    ClassX['value'] == ClassX('value', IndexOrAccessToInstantiate.ITEM)

    In order for this metaclass to function correctly any class that makes use
    of it needs to ensure its __init__ function is correctly defined to handle
    the behaviour demonstrated above.
    """
    ATTR = 'attr'
    ITEM = 'item'

    def __getattr__(cls, name):
        return cls(name, IndexOrAccessToInstantiate.ATTR)

    def __getitem__(cls, name):
        return cls(name, IndexOrAccessToInstantiate.ITEM)
