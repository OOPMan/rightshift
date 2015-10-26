from rightshift import Transformer, TransformationException, Chain, \
    ChainException
from future.utils import raise_from

__author__ = 'adam.jorgensen.za@gmail.com'


class ExtractorException(TransformationException): pass


class Extractor(Transformer): pass


class Identity(Extractor):
    """
    The IdentityExtractor is extremely simple and simply returns whatever
    value it is called with. However, it does inherit from the Extractor
    class and hence inherits the & and | functionality implement by the
    Extractor class.
    """
    def __call__(self, value, **flags):
        return value


identity = Identity()


class ItemChainException(ChainException): pass


class ItemChain(Chain):
    """
    TODO: Document
    """
    def __getattr__(self, item_name):
        """
        :param item_name: A valid item name value
        :return: an ItemChain instance
        :rtype: ItemChain
        """
        return self.__getitem__(item_name)

    def __getitem__(self, item_or_slice):
        """
        :param item_or_slice: A valid item name or slice value
        :return: an ItemChain instance
        :rtype: ItemChain
        """
        return ItemChain(self, Item(item_or_slice))


class Item(Extractor):
    """
    An ItemExtractor instances expects to be called with a value that will be
    accessed as if it were a container type in order to retrieve the item or
    slice that the ItemExtract was instantiated with.

    If retrieval of the item fails from the value then an ExtractorException
    is raised.
    """
    def __init__(self, item_or_slice):
        """
        :param item_or_slice: A valid item name or slice value
        """
        self.item_or_slice = item_or_slice

    def __call__(self, value, **flags):
        """
        :param value: The value to attempt extraction from
        :param flags: A dictionary of flags
        :return: The extracted value
        :raise: ExtractorException
        """
        try:
            return value[self.item_or_slice]
        except Exception as e:
            raise_from(ExtractorException, e)

    def __getattr__(self, item_name):
        """
        :param item_name: A valid item name value
        :return: an ItemChain instance
        :rtype: ItemChain
        """
        return self.__getitem__(item_name)

    def __getitem__(self, item_or_slice):
        """
        :param item_or_slice: A valid item name or slice value
        :return: an ItemChain instance
        :rtype: ItemChain
        """
        return ItemChain(self, Item(item_or_slice))


class __ItemCreator(object):
    """
    The _ItemCreator is a private class that is instantiated once
    and assigned to the `item` variable in the rightshift.extractors module.

    This allows syntax of the form item['key'], item.key and item('key') to be
    used in place of the less compact Item('key') form.
    """
    def __call__(self, item_or_slice):
        """
        :param item_or_slice: A valid item name or slice value
        :return: an Item instance
        :rtype: Item
        """
        return self.__getitem__(item_or_slice)

    def __getattr__(self, item_name):
        """
        :param item_name: A valid item name value
        :return: an Item instance
        :rtype: Item
        """
        return self.__getitem__(item_name)

    def __getitem__(self, item_or_slice):
        """
        :param item_or_slice: A valid item name or slice value
        :return: an Item instance
        :rtype: Item
        """

        return Item(item_or_slice)


item = __ItemCreator()
"""
item is a special shortcut to enable working with the Item class to
feel more natural. item is an instance of the private __ItemCreator
class which mirrors the functionality of the Item class but is not
actually an instance of Item itself. This allows item to be used to
generate natural looking item extraction expressions.

Examples:

item['x'] is equivalent to Item('x')
item['x']['y'] is equivalent to Item('x')['y']
"""


class AttributeChainException(ChainException): pass


class AttributeChain(Chain):
    """
    TODO: Document
    """
    def __getattr__(self, attribute):
        """
        :param attribute: A valid attribute name value
        :return: an AttributeChain instance
        :rtype: AttributeChain
        """
        return self.__getitem__(attribute)

    def __getitem__(self, attribute):
        """
        :param attribute: A valid attribute name value
        :return: an AttributeChain instance
        :rtype: AttributeChain
        """
        return AttributeChain(self, Attribute(attribute))


class Attribute(Extractor):
    """
    An AttributeExtractor instance can be called with a value in order to
    attempt to retrieve an attribute on that value.

    If retrieval of the attribute fails from the value then an ExtractorException
    is raised.
    """
    def __init__(self, attribute):
        """
        :param attribute: A valid attribute name value
        """
        self.attribute = attribute

    def __call__(self, value, **flags):
        """
        :param value: The value to attempt extraction from
        :param flags: A dictionary of flags
        :return: The extracted value
        :raise: ExtractorException
        """
        if hasattr(value, self.attribute):
            return getattr(value, self.attribute)
        else:
            raise ExtractorException('{} has no attribute `{}`'.format(value, self.attribute))

    def __getitem__(self, attribute):
        """
        :param attribute: A valid attribute name value
        :return: an AttributeChain instance
        :rtype: AttributeChain
        """
        return self.__getattr__(attribute)

    def __getattr__(self, attribute):
        """
        :param attribute: A valid attribute name value
        :return: an AttributeChain instance
        :rtype: AttributeChain
        """
        return AttributeChain(self, Attribute(attribute))


class __AttributeCreator(object):
    """
    The _AttributeCreator is a private class that is instantiated once
    and assigned to the `attr` variable in the rightshift.extractors module.

    This allows syntax of the form item['key'], item.key and item('key') to be
    used in place of the less compact Item('key') form.
    """
    def __call__(self, attribute):
        """
        :param attribute: A valid attribute name value
        :return: an AttributeExtractor instance
        :rtype: Attribute
        """
        return self.__getattr__(attribute)

    def __getitem__(self, attribute):
        """
        :param attribute: A valid attribute name value
        :return: an AttributeExtractor instance
        :rtype: Attribute
        """
        return self.__getattr__(attribute)

    def __getattr__(self, attribute):
        """
        :param attribute: A valid attribute name value
        :return: an AttributeExtractor instance
        :rtype: Attribute
        """

        return Attribute(attribute)

    def __setattr__(self, key, value):
        """
        :raise: NotImplementedError
        """
        raise NotImplementedError

attr = __AttributeCreator()
"""
attr is a special shortcut to enable working with the Attribute class
to feel more natural. attr is an instance of the private __AttributeCreator
class which mirrors the functionality of the Attribute class but is not
actually an instance of Attribute itself. This allows attr to be used
to generate natural looking attr extraction expressions.

Examples:

attr.x is equivalent to Item('x')
attr.x.y is equivalent to Item('x').y
"""


class PatternGroup(Extractor):
    def __init__(self, pattern, group=1, search=True):
        """
        :param pattern: A string or compiled Regular Expression pattern
        :param group: A string or numeric group value
        :param search: A boolean value indicating whether the search or match method should be used
        """
        from past.builtins import basestring
        if isinstance(pattern, basestring):
            from re import compile
            pattern = compile(pattern)
        self.pattern = pattern
        self.group = group
        self.search = search

    def __call__(self, value, **flags):
        try:
            method = self.pattern.search if flags.get('pattern_group__search', self.search) else self.pattern.match
            match = method(value)
            if match is None:
                raise ExtractorException
            return match.group(flags.get('pattern_group__group', self.group))
        except Exception as e:
            raise_from(ExtractorException, e)

pattern_group = PatternGroup
"""
TODO: Document
"""

