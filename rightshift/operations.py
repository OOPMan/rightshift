from rightshift import Transformer, RightShiftException

__author__ = 'adam.jorgensen.za@gmail.com'


class OperationException(RightShiftException):
    pass


class Operation(Transformer):
    """
    Transformers that implement operator-like functionality should inherit
    from this class
    """
    pass


class UnaryOperation(Operation):
    """
    Operations that are unary in nature inherit from this class
    """
    pass


class BinaryOperation(Operation):
    """
    Operations are are binary in nature inherit from this class
    """
    def __init__(self, value):
        self.value = value


class ArithmeticOperation(Operation):
    """
    Arithmetic operations inherit from this class. The difference between this
    class and BinaryOperation is that it accepts multiple input values which
    allows for usages like:

    add(1,2,3)(0) == 6 compared to (add(1) >> add(2) add(3))(0) == 6
    """
    def __init__(self, *values):
        self.values = values


class NegationOperation(UnaryOperation):
    """
    Implements the negation operator
    """
    def __call__(self, value):
        return -value

negate = NegationOperation = NegationOperation()


class PositiveOperation(UnaryOperation):
    """
    Implements the positive operator
    """
    def __call__(self, value):
        return +value

positive = PositiveOperation = PositiveOperation()


class AbsoluteOperation(UnaryOperation):
    """
    Implements the absolute value operation
    """
    def __call__(self, value):
        return abs(value)

absolute = AbsoluteOperation = AbsoluteOperation()


class InvertOperation(UnaryOperation):
    """
    Implements the inversion operator
    """
    def __call__(self, value):
        return ~value

invert = InvertOperation = InvertOperation()


class LogicalNotOperation(UnaryOperation):
    """
    Implements the logical not operation
    """
    def __call__(self, value):
        return not value

logical_not = LogicalNotOperation


class FloorModuloOperation(BinaryOperation):
    """
    Implements the floor division // operator
    """
    def __call__(self, value, **flags):
        return value // self.value

floor_mod = floor_modulo = floor_divide = FloorModuloOperation


class ModuloOperation(BinaryOperation):
    """
    Implements the modulo % operator
    """
    def __call__(self, value, **flags):
        return value % self.value

mod = modulo = ModuloOperation


class DivModOperation(BinaryOperation):
    """
    Implements the divmod operation
    """
    def __call__(self, value, **flags):
        return divmod(value, self.value)

div_mod = DivModOperation


class AddOperation(ArithmeticOperation):
    """
    Implements the add + operator
    """
    def __call__(self, value, **flags):
        for v in self.values:
            value += v
        return value

add = AddOperation


class SubtractOperation(ArithmeticOperation):
    """
    Implements the subtract - operator
    """
    def __call__(self, value, **flags):
        for v in self.values:
            value -= v
        return value

sub = subtract = SubtractOperation


class MultiplyOperation(ArithmeticOperation):
    """
    Implements the multiply * operator
    """
    def __call__(self, value, **flags):
        for v in self.values:
            value *= v
        return value

mul = multiply = MultiplyOperation


class DivideOperation(ArithmeticOperation):
    """
    Implements the / divide operator
    """
    def __call__(self, value, **flags):
        for v in self.values:
            value /= v
        return value

div = divide = true_divide = DivideOperation


class PowOperation(ArithmeticOperation):
    """
    Implements the pow operation
    """
    def __init__(self, *values):
        if len(values) > 2:
            raise OperationException('A maximum of 2 parameters may be supplied '
                                     'to rightshift.operations.PowOperation')
        super(PowOperation, self).__init__(*values)

    def __call__(self, value, **flags):
        return pow(value, *self.values)

power = raise_to = PowOperation


class LeftShiftOperation(ArithmeticOperation):
    """
    Implements the left shift << operator
    """
    def __call__(self, value, **flags):
        for v in self.values:
            value <<= v
        return value

left_shift = lshift = LeftShiftOperation


class RightShiftOperation(ArithmeticOperation):
    """
    Implements the right shift >> operator
    """
    def __call__(self, value, **flags):
        for v in self.values:
            value >>= v
        return value

right_shift = rshift = RightShiftOperation


class AndOperation(ArithmeticOperation):
    """
    Implements the bitwise and & operator
    """
    def __call__(self, value, **flags):
        for v in self.values:
            value &= v
        return value

bitwise_and = AndOperation


class OrOperation(ArithmeticOperation):
    """
    Implements the bitwise | operator
    """
    def __call__(self, value, **flags):
        for v in self.values:
            value |= v
        return value

bitwise_or = OrOperation


class XorOperation(ArithmeticOperation):
    """
    Implements the bitwise xor ^ operator
    """
    def __call__(self, value, **flags):
        for v in self.values:
            value ^= v
        return value

xor = bitwise_xor = XorOperation


class CallOperation(Operation):
    """
    The call operation can be used to call the value it receives with the
    parameters supplied to the constructor. Eg.

    call(1,2,3)(sum) == 6
    """
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def __call__(self, value, **kwargs):
        return value(*self.args, **self.kwargs)

call = CallOperation
