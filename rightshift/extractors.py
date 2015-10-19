from rightshift import Transformer, TransformationException
from future.utils import raise_from

__author__ = 'adam.jorgensen.za@gmail.com'


class ExtractorException(TransformationException):
    pass


class Extractor(Transformer):

    def __ror__(self, other):
        if isinstance(other, Extractor):
            # TODO: ORing two Extractor type Transforms causes the first
            # TODO: successfully extracted result to be returned
            pass
        pass

    def __rand__(self, other):
        if isinstance(other, Extractor):
            # TODO: ANDing two Extractor type Transforms causes each Transform
            # TODO: to be executed and the extracted results return as a list.
            # TODO: Repeated ANDs stack such that the result of a & b & c will
            # TODO: be a flat list with 3 elements of the form [a(), b(), c(0]
            # TODO: rather than a nested list of the form [a(), [b(), c()]]
            pass
        pass


class _IdentityExtractor(Extractor):
    """
    The IdentityExtractor is extremely simple and simply returns whatever
    value it is called with. However, it does inherit from the Extractor
    class and hence inherits the & and | functionality implement by the
    Extractor class.
    """
    def __call__(self, value, **flags):
        return value
identity = _IdentityExtractor()


class _ItemExtractor(Extractor):
    """
    An ItemExtractor instances expects to be called with a value that will be
    accessed as if it were a container type in order to retrieve the item or
    slice that the ItemExtract was instantiated with.

    If retrieval of the item fails from the value then a TransformationException
    is raised.
    """

    def __init__(self, item=None):
        self.item = item

    def __call__(self, value, **flags):
        try:
            return value[self.item]
        except Exception as e:
            raise_from(ExtractorException, e)

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

    def __call__(self, value, **flags):
        try:
            method = self.pattern.search if self.search else self.pattern.match
            match = method(value)
            if match is None:
                raise ExtractorException
            return match.group(self.group)
        except Exception as e:
            raise_from(ExtractorException, e)
pattern_group = _PatternGroupExtractor


