from rightshift import Transformer, TransformationException
from future.utils import raise_from

__author__ = 'adam.jorgensen.za@gmail.com'


class ExtractorException(TransformationException):
    pass


class Extractor(Transformer):
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


def identity():
    class IdentityExtractor(_IdentityExtractor):
        pass

    return IdentityExtractor()


class _ItemExtractor(Extractor):
    """
    An ItemExtractor instances expects to be called with a value that will be
    accessed as if it were a container type in order to retrieve the item or
    slice that the ItemExtract was instantiated with.

    If retrieval of the item fails from the value then a TransformationException
    is raised.
    """

    def __getitem__(self, item):
        class ItemExtractor(_ItemExtractor):
            def __call__(self, value, **flags):
                try:
                    return value[item]
                except Exception as e:
                    raise_from(ExtractorException, e)
        return ItemExtractor()

item = _ItemExtractor()


class _PatternGroupExtractor(Extractor):
    pass


def pattern_group(pattern, group=1, search=True):
    from past.builtins import basestring
    if isinstance(pattern, basestring):
        from re import compile
        pattern = compile(pattern)

    class PatternGroupExtractor(_PatternGroupExtractor):
        def __call__(self, value, **flags):
            try:
                method = pattern.search if search else pattern.match
                match = method(value)
                if match is None:
                    raise ExtractorException
                return match.group(group)
            except Exception as e:
                raise_from(ExtractorException, e)

    return PatternGroupExtractor()


