from hypothesis import given, assume
from hypothesis.strategies import none, text, integers, floats, complex_numbers
from hypothesis.strategies import booleans, tuples, lists, sets, frozensets
from hypothesis.strategies import dictionaries, binary, fractions, decimals
from hypothesis.strategies import one_of
from math import isnan
from cmath import isnan as isnanj

from rightshift import identity


@given(none())
def test_identity_with_none(data):
    assert identity(data) == data
    assert (identity >> identity)(data) == data


@given(text())
def test_identity_with_text(data):
    assert identity(data) == data
    assert (identity >> identity)(data) == data


@given(integers())
def test_identity_with_integers(data):
    assert identity(data) == data
    assert (identity >> identity)(data) == data


@given(floats())
def test_identity_with_floats(data):
    assume(not isnan(data))
    assert identity(data) == data
    assert (identity >> identity)(data) == data


@given(complex_numbers())
def test_identity_with_complex_numbers(data):
    assume(not isnanj(data))
    assert identity(data) == data
    assert (identity >> identity)(data) == data


@given(booleans())
def test_identity_with_booleans(data):
    assert identity(data) == data
    assert (identity >> identity)(data) == data


@given(binary())
def test_identity_with_binary(data):
    assert identity(data) == data
    assert (identity >> identity)(data) == data


@given(decimals())
def test_identity_with_decimals(data):
    assume(not isnan(data))
    assert identity(data) == data
    assert (identity >> identity)(data) == data


@given(fractions())
def test_identity_with_fractions(data):
    assert identity(data) == data
    assert (identity >> identity)(data) == data


@given(lists(integers()))
def test_identity_with_lists_of_integers(data):
    assert identity(data) == data
    assert (identity >> identity)(data) == data


@given(sets(integers()))
def test_identity_with_sets_of_integers(data):
    assert identity(data) == data
    assert (identity >> identity)(data) == data


@given(frozensets(integers()))
def test_identity_with_frozensets_of_integers(data):
    assert identity(data) == data
    assert (identity >> identity)(data) == data


@given(tuples(text(), integers(), floats()))
def test_identity_with_sets_of_tuples(data):
    assert identity(data) == data
    assert (identity >> identity)(data) == data


@given(dictionaries(one_of(text(), integers()), one_of(integers(), text())))
def test_identity_with_dictionaries(data):
    assert identity(data) == data
    assert (identity >> identity)(data) == data
