from math import isnan

from rightshift.extractors import item, attr, pattern_group
from hypothesis import given, assume
from hypothesis.strategies import text, integers, floats, lists, booleans, one_of
from random import randint


def __common_item_tests(data):
    assume(len(data) > 0)
    index = randint(0, len(data) - 1)
    if isinstance(data[index], float):
        assume(not isnan(data[index]))
    assert item[index](data) == data[index]


@given(text())
def test_item_with_text(data):
    __common_item_tests(data)


@given(lists(one_of(text(), integers(), floats(), booleans())))
def test_item_with_lists(data):
    __common_item_tests(data)


