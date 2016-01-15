from hypothesis import given, assume
from hypothesis.strategies import text, booleans, integers, floats, one_of, just

from rightshift.matchers import must, should, must_not, is_instance, comparison
from rightshift.matchers import lt, lte, eq, ne, gte, gt, value_is, between, matches_regex


@given(one_of(text(), booleans(), floats(), integers()))
def test_is_instance_with_text_floats_booleans_integers(data):
    data_type = type(data)
    assert is_instance(data_type)(data) == isinstance(data, data_type)


@given(text(min_size=1), text(min_size=1))
def test_matches_regex_with_text(prefix, postfix):
    constant = 'a constant string'
    variants = [
        constant,
        prefix + constant,
        constant + postfix,
        prefix + constant + postfix
    ]
    for variant in variants:
        assert matches_regex(constant)(variant)


@given(integers())
def test_comparisons_with_integers(x):

    @given(just(x), integers(max_value=x - 1))
    def test_lt(a, b):
        assert b < a
        assert lt(a)(b)
        assert (value_is < a)(b)

    @given(just(x), integers(max_value=x))
    def test_lte(a, b):
        assert b <= a
        assert lte(a)(b)
        assert (value_is <= a)(b)

    @given(just(x), just(x))
    def test_eq(a, b):
        assert a == b
        assert eq(a)(b)
        assert (value_is == a)(b)

    @given(just(x), integers())
    def test_ne(a, b):
        assume(a != b)
        assert a != b
        assert ne(a)(b)
        assert (value_is != a)(b)

    @given(just(x), integers(min_value=x))
    def test_gte(a, b):
        assert b >= a
        assert gte(a)(b)
        assert (value_is >= a)(b)

    @given(just(x), integers(min_value=x+1))
    def test_gt(a, b):
        assert b > a
        assert gt(a)(b)
        assert (value_is > a)(b)

    @given(integers(max_value=x-1), just(x), integers(min_value=x+1))
    def test_between(a, b, c):
        assert a < b < c
        assert between(a, c)(b)
        assert must(gt(a), lt(c))(b)
        assert ((value_is > a) & (value_is < c))(b)

    test_lt()
    test_lte()
    test_eq()
    test_ne()
    test_gte()
    test_gt()
    test_between()

