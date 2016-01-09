from math import isnan
from hypothesis import given, assume
from hypothesis.strategies import text, integers, floats, lists, booleans
from hypothesis.strategies import dictionaries, one_of
from random import randint, choice
from past.builtins import basestring
from string import letters, digits

from rightshift.extractors import item, attr, pattern_group


def __common_item_tests(data, index=None):
    assume(len(data) > 0)
    if index is None:
        index = randint(0, len(data) - 1)
    if isinstance(data[index], float):
        assume(not isnan(data[index]))
    assert item[index](data) == data[index]
    if isinstance(index, basestring):
        assert getattr(item, index)(data) == data[index]


@given(text())
def test_item_with_text(data):
    __common_item_tests(data)


@given(lists(one_of(text(), integers(), floats(), booleans())))
def test_item_with_lists(data):
    __common_item_tests(data)


@given(dictionaries(keys=text(alphabet=letters + digits),
                    values=one_of(text(), integers(), floats(), booleans()),
                    min_size=1))
def test_item_with_dictionaries(data):
    key = choice(data.keys())
    __common_item_tests(data, key)


