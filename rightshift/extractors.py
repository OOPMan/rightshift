from future.utils import raise_from

from rightshift import Transformer, TransformationException, Chain, HasFlags
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
    """
    TODO: Document
    """

    def __init__(self):
        super(ItemMixin, self).__init__()
        self.chain_class = ItemChain
        self.class_ = Item


class ItemChain(Chain, ItemMixin):
    """
    A chain of Item extractors.
    """


class Item(HasFlags(Extractor, ItemMixin, metaclass=IndexOrAccessToInstantiate)):
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

    def __init__(self, item_or_slice, _):
        """
        :param item_or_slice: A valid item name or slice value
        """
        super(Item, self).__init__()
        self.item_or_slice = item_or_slice

    def __call__(self, value, flags):
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


item = items = Item
"""
item and items are aliases to the Item class.
"""


class AttributeMixin(IndexOrAccessToChainMixin):
    """
    TODO: Document
    """

    def __init__(self):
        super(AttributeMixin, self).__init__()
        self.chain_class = AttributeChain
        self.class_ = Attribute


class AttributeChain(Chain, AttributeMixin):
    """
    A chain of Attribute extractors.
    """


class Attribute(HasFlags(Extractor, AttributeMixin, metaclass=IndexOrAccessToInstantiate)):
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

    def __init__(self, attribute, _):
        """
        :param attribute: A valid attribute name value
        """
        super(Attribute, self).__init__()
        self.attribute = attribute

    def __call__(self, value, flags):
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


class ObjectMixin(IndexOrAccessToChainMixin):
    """
    TODO: Document
    """

    def __init__(self):
        super(AttributeMixin, self).__init__()
        self.chain_class = ObjectChain
        self.class_ = Object


class ObjectChain(Chain, ObjectMixin):
    """
    A chain of Object extractors
    """
    pass


class Object(HasFlags(Extractor, ObjectMixin, metaclass=IndexOrAccessToInstantiate)):
    """
    An Object instance can be called with a value in order to retrieve an item,
    slice or attribute on that value.

    This class makes use of the functionality defined by the Attribute and Item
    classes in this module and behaves in a similar fashion except that whereas
    with Attribute and Item the indexing and attribute addressing methods may
    be freely mixed, with this class the addressing method determines whether
    the Item or Attribute class is used to extract data.
    """

    def __init__(self, item_or_attribute, determiner):
        super(Object, self).__init__()
        self.attribute = item_or_attribute
        self.item_or_slice = item_or_attribute
        self.determiner = determiner

    def __call__(self, value, flags):
        if self.determiner == IndexOrAccessToInstantiate.ATTR:
            return Attribute.__call__(self, value, **flags)
        elif self.determiner == IndexOrAccessToInstantiate.ITEM:
            return Item.__call__(self, value, **flags)
        raise ExtractorException('self.determiner is not a valid value: '
                                 '{}'.format(self.determiner))


obj = Object
"""
obj is an alias to Object
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

    def __call__(self, value, flags):
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
pattern_group is an alias to the PatternGroup class
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

    def __call__(self, value, flags):
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
"""
coerce_to is an alias to the CoerceTo class
"""


