from hypothesis import given, assume
from hypothesis.strategies import none, text, integers, floats, complex_numbers
from hypothesis.strategies import booleans, tuples, lists, sets, frozensets
from hypothesis.strategies import dictionaries, binary, fractions, decimals
from hypothesis.strategies import one_of
from math import isnan
from cmath import isnan as iscnan

from rightshift import identity, value, wrap


def __common_identity_tests(data):
    """
    Generally the operations performed with identity should be simple enough
    that they behave the same regardless of the input (Barring some minor
    exceptions like NaN). As a result, all of the assertions used to test
    the identity transform are performed in this common function.

    :param data:
    :return:
    """
    assert identity(data) == data
    assert (identity >> identity)(data) == data
    assert (identity & identity)(data) == [data, data]
    assert (identity | identity)(data) == data
    assert (identity & identity | identity)(data) == [data, data]
    assert (identity | identity & identity)(data) == data


@given(none())
def test_identity_with_none(data):
    __common_identity_tests(data)


@given(text())
def test_identity_with_text(data):
    __common_identity_tests(data)


@given(integers())
def test_identity_with_integers(data):
    __common_identity_tests(data)


@given(floats())
def test_identity_with_floats(data):
    assume(not isnan(data))
    __common_identity_tests(data)


@given(complex_numbers())
def test_identity_with_complex_numbers(data):
    assume(not iscnan(data))
    __common_identity_tests(data)


@given(booleans())
def test_identity_with_booleans(data):
    __common_identity_tests(data)


@given(binary())
def test_identity_with_binary(data):
    __common_identity_tests(data)


@given(decimals())
def test_identity_with_decimals(data):
    assume(not isnan(data))
    __common_identity_tests(data)


@given(fractions())
def test_identity_with_fractions(data):
    __common_identity_tests(data)


@given(lists(integers()))
def test_identity_with_lists_of_integers(data):
    __common_identity_tests(data)


@given(sets(integers()))
def test_identity_with_sets_of_integers(data):
    __common_identity_tests(data)


@given(frozensets(integers()))
def test_identity_with_frozensets_of_integers(data):
    __common_identity_tests(data)


@given(tuples(text(), integers(), floats()))
def test_identity_with_sets_of_tuples(data):
    __common_identity_tests(data)


@given(dictionaries(one_of(text(), integers()), one_of(integers(), text())))
def test_identity_with_dictionaries(data):
    __common_identity_tests(data)


def __common_value_tests(data):
    """
    Generally the operations performed with value should be simple enough
    that they behave the same regardless of the input (Barring some minor
    exceptions like NaN). As a result, all of the assertions used to test
    the value transform are performed in this common function.

    :param data:
    :return:
    """
    assert value(data)(None) == data
    assert (value(data) >> value(data))(None) == data
    assert (value(data) & value(data))(None) == [data, data]
    assert (value(data) | value(data))(None) == data
    assert (value(data) & value(data) | value(data))(None) == [data, data]
    assert (value(data) | value(data) & value(data))(None) == data


@given(text())
def test_value_with_text(data):
    __common_value_tests(data)


@given(integers())
def test_value_with_integers(data):
    __common_value_tests(data)


@given(floats())
def test_value_with_floats(data):
    assume(not isnan(data))
    __common_value_tests(data)


@given(complex_numbers())
def test_value_with_complex_numbers(data):
    assume(not iscnan(data))
    __common_value_tests(data)


@given(booleans())
def test_value_with_booleans(data):
    __common_value_tests(data)


@given(binary())
def test_value_with_binary(data):
    __common_value_tests(data)


@given(decimals())
def test_value_with_decimals(data):
    assume(not isnan(data))
    __common_value_tests(data)


@given(fractions())
def test_value_with_fractions(data):
    __common_value_tests(data)


@given(lists(integers()))
def test_value_with_lists_of_integers(data):
    __common_value_tests(data)


@given(sets(integers()))
def test_value_with_sets_of_integers(data):
    __common_value_tests(data)


@given(frozensets(integers()))
def test_value_with_frozensets_of_integers(data):
    __common_value_tests(data)


@given(tuples(text(), integers(), floats()))
def test_value_with_sets_of_tuples(data):
    __common_value_tests(data)


@given(dictionaries(one_of(text(), integers()), one_of(integers(), text())))
def test_value_with_dictionaries(data):
    __common_value_tests(data)


@given(integers())
def test_wrap_with_integers(data):
    assert wrap(lambda i: i * i)(data) == data * data
    assert (wrap(lambda i: i * i) >> wrap(lambda i: i * i))(data) == data * data * data * data
