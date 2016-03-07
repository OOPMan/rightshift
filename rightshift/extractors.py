from future.utils import raise_from

from rightshift import Transformer, TransformationException, Chain
from rightshift.chains import IndexOrAccessToChainMixin
from rightshift.magic import IndexOrAccessToInstantiate

__author__ = 'adam.jorgensen.za@gmail.com'


class ExtractorException(TransformationException):
    """
    Base class for all Exceptions thrown by components of this module.
    """


class Extractor(Transformer):
    """
    Base class for all Transformers defined in this module. If you are writing
    a new Transformer that that fits the general description of an Extractor
    then it should inherit from this class.
    """


class ItemMixin(IndexOrAccessToChainMixin):
    __chain_class = ItemChain
    __class = Item


class ItemChain(Chain, ItemMixin):
    """
    TODO: Document
    """


class Item(Extractor, ItemMixin):
    """
    An Item instances expects to be called with a value that will be
    accessed as if it were a container type in order to retrieve the item or
    slice that the ItemExtract was instantiated with.

    If retrieval of the item fails from the value then an ExtractorException
    is raised.

    Examples:

    Item('x')
    Item.x
    Item['x']
    Item.x.y
    Item['x']['y']
    Item[variable]
    Item[42]
    """
    __metaclass__ = IndexOrAccessToInstantiate

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


item = Item
"""
item is an alias to the Item class.
"""


class AttributeMixin(IndexOrAccessToChainMixin):
    __chain_class = AttributeChain
    __class = Attribute


class AttributeChain(Chain, AttributeMixin):
    """
    TODO: Document
    """


class Attribute(Extractor, AttributeMixin):
    """
    An Attribute instance can be called with a value in order to
    attempt to retrieve an attribute on that value.

    If retrieval of the attribute fails from the value then an ExtractorException
    is raised.

    Examples:

    Attribute('x')
    Attribute.x
    Attribute['x']
    Attribute('x').y
    Attribute.x.y
    Attribute['x']['y']
    Attribute[variable]
    """
    __metaclass__ = IndexOrAccessToInstantiate

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

attr = prop = Attribute
"""
attr and prop are aliases to the Attribute class.
"""


class PatternGroup(Extractor):
    """
    A PatternGroup can be called with a string in order to attempt to extract a
    new string from that string using a regular expression.
    """
    def __init__(self, pattern, group=1, search=True):
        """
        :param pattern: A string or compiled Regular Expression pattern
        :param group: A string or numeric group value
        :param search: A boolean value indicating whether the search or match
                       method should be used
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


class CoerceTo(Extractor):
    """
    A CoerceTo instance will attempt to transform the type of an input value.
    """
    def __init__(self, type, coercer=None):
        if type is None and coercer is None:
            coercer = lambda v: None
        if coercer is None:
            coercer = type
        self.type = type
        self.coercer = coercer

    def __call__(self, value, **flags):
        try:
            value = self.coercer(value)
            if not isinstance(value, self.type):
                raise ExtractorException('Unable to coerce {} to {}'.format(
                    value, self.type))
        except ExtractorException:
            raise
        except Exception as e:
            raise_from(ExtractorException, e)
        return value

coerce_to = CoerceTo


