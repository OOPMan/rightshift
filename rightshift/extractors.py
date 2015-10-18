from rightshift import Transformer, TransformationException
from future.utils import raise_from

__author__ = 'adam.jorgensen.za@gmail.com'


class Extractor(Transformer):
    pass


class _ItemExtractor(Extractor):
    """
    An ItemExtract instances expects to be called with a value that will be
    accessed as if it were a container type in order to retrieve the item or
    slice that the ItemExtract was instantiated with.

    If retrieval of the item fails from the value then a TransformationException
    is raised.
    """

    def __init__(self, item=None):
        self.item = item

    def __call__(self, value):
        try:
            return value[self.item]
        except Exception as e:
            raise_from(TransformationException, e)

    def __getitem__(self, item):
        return _ItemExtractor(item)
item = _ItemExtractor()


class _PatternGroupExtractor(Extractor):

    def __init__(self, pattern, group=1, search=True):
        from past.builtins import basestring
        if isinstance(pattern, basestring):
            from re import compile
            pattern = compile(pattern)
        self.pattern = pattern
        self.group = group
        self.search = search

    def __call__(self, value):
        try:
            method = self.pattern.search if self.search else self.pattern.match
            match = method(value)
            if match is None:
                raise TransformationException
            return match.group(self.group)
        except Exception as e:
            raise_from(TransformationException, e)
pattern_group = _PatternGroupExtractor


