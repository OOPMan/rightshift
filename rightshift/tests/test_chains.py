from rightshift import Transformer, TransformationException
from rightshift.chains import flags, default
from hypothesis import given
from hypothesis.strategies import text, integers, floats


class DefaultTestTransform(Transformer):
    def __call__(self, value, **flags):
        raise TransformationException()
raises_transformation_exception = DefaultTestTransform()


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
    __common_default_tests(a, b)

