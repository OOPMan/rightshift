from hypothesis import given
from hypothesis.strategies import none, text

from rightshift import identity


@given(none())
def test_identity_with_none(data):
    assert identity(data) == data
    assert (identity >> identity)(data) == data


@given(text())
def test_identity_with_text(data):
    assert identity(data) == data
    assert (identity >> identity)(data) == data


