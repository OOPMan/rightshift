from math import isnan

from rightshift import Transformer, TransformationException
from rightshift.chains import flags, default
from hypothesis import given, assume
from hypothesis.strategies import text, integers, floats


class DefaultTestTransform(Transformer):
    def __call__(self, value, **flags):
        raise TransformationException()
raises_transformation_exception = DefaultTestTransform()


class FlagsTestTransform(Transformer):
    def __call__(self, value, **flags):
        return flags.get('override', value)
returns_override_value_from_flags = FlagsTestTransform()


def __common_default_tests(a, b):
    assert (raises_transformation_exception >> default(a))(b) == a
    assert (raises_transformation_exception >> default(b))(a) == b


@given(text(), text())
def test_default_with_text(a, b):
    __common_default_tests(a, b)


@given(integers(), integers())
def test_default_with_integers(a, b):
    __common_default_tests(a, b)


@given(floats(), floats())
def test_default_with_floats(a, b):
    assume(not isnan(a))
    assume(not isnan(b))
    __common_default_tests(a, b)


def __common_flag_tests(a, b):
    assert (returns_override_value_from_flags >> flags(override=a))(b) == a
    assert (returns_override_value_from_flags >> flags(override=b))(a) == b


@given(text(), text())
def test_flags_with_text(a, b):
    __common_flag_tests(a, b)


@given(integers(), integers())
def test_flags_with_integers(a, b):
    __common_flag_tests(a, b)


@given(floats(), floats())
def test_flags_with_floats(a, b):
    assume(not isnan(a))
    assume(not isnan(b))
    __common_flag_tests(a, b)
