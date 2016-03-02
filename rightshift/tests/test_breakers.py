from unittest import TestCase
from hypothesis import given
from hypothesis.strategies import text
from rightshift import identity
from rightshift.matchers import is_instance
from rightshift.breakers import break_if, break_if_not, BreakerException


class BreakersTest(TestCase):

    @given(text())
    def test_break_if_with_text(self, data):
        data_type = type(data)
        self.assertRaises(BreakerException, identity >> break_if(is_instance(data_type)), data)


@given(text())
def test_break_if_not_with_text(data):
    data_type = type(data)
    f = identity >> break_if_not(is_instance(data_type))
    assert(f(data), data)
