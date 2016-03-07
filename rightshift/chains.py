from copy import copy
from rightshift import Chain, ChainTransformer, TransformationException

__author__ = 'adam.jorgensen.za@gmail.com'


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

    def __lshift__(self, other):
        return self.left >> other >> Flags(**self.flags)


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
flags is an alias to the Flags class.
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

    def __lshift__(self, other):
        return self.left >> other >> Default(self.default)


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
default is an alias to the Default class.
"""


class IndexOrAccessToChainMixin(object):
    """

    """
    __chain_class = None
    __class = None

    def __getattr__(self, item_name):
        """
        :param item_name: A valid item name value
        :return: an ItemChain instance
        :rtype: ItemChain
        """
        return self.__chain_class(self, self.__class(item_name))

    def __getitem__(self, item_or_slice):
        """
        :param item_or_slice: A valid item name or slice value
        :return: an ItemChain instance
        :rtype: ItemChain
        """
        return self.__chain_class(self, self.__class(item_or_slice))
