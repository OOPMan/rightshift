from rightshift import Transformer, TransformationException
from future.utils import raise_from

__author__ = 'adam.jorgensen.za@gmail.com'


class _ItemExtractor(Transformer):
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




