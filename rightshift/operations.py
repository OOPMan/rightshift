from rightshift import Transformer, RightShiftException

__author__ = 'adam.jorgensen.za@gmail.com'


class OperationException(RightShiftException):
    pass


class Operation(Transformer):
    pass


class BinaryOperation(Operation):
    def __init__(self, value):
        self.value = value


class ArithmeticOperation(Operation):
    def __init__(self, *values):
        self.values = values


class AddOperation(ArithmeticOperation):

    def __call__(self, value, **flags):
        return sum(self.values, value)

add = AddOperation


class SubtractOperation(ArithmeticOperation):
    def __call__(self, value, **flags):
        return value - sum(self.values)

sub = subtract = SubtractOperation


class MultiplyOperation(ArithmeticOperation):
    def __call__(self, value, **flags):
        for v in self.values:
            value *= v
        return value

mul = multiply = MultiplyOperation


class DivideOperation(ArithmeticOperation):
    def __call__(self, value, **flags):
        for v in self.values:
            value /= v
        return value

div = divide = DivideOperation


class FloorModuloOperation(BinaryOperation):
    def __call__(self, value, **flags):
        return value // self.value

floor_mod = floor_modulo = FloorModuloOperation


class ModuloOperation(BinaryOperation):
    def __call__(self, value, **flags):
        return value % self.value

mod = modulo = ModuloOperation


class DivModOperation(BinaryOperation):
    def __call__(self, value, **flags):
        return divmod(value, self.value)

div_mod = DivModOperation


class PowOperation(ArithmeticOperation):
    def __init__(self, *values):
        if len(values) > 2:
            raise OperationException('A maximum of 2 parameters may be supplied '
                                     'to rightshift.operations.PowOperation')
        super(PowOperation, self).__init__(*values)

    def __call__(self, value, **flags):
        return pow(value, *self.values)

power = raise_to = PowOperation


class LeftShiftOperation(ArithmeticOperation):
    def __call__(self, value, **flags):
        for v in self.values:
            value <<= v
        return value

left_shift = lshift = LeftShiftOperation


class RightShiftOperation(ArithmeticOperation):
    def __call__(self, value, **flags):
        for v in self.values:
            value >>= v
        return value

right_shift = rshift = RightShiftOperation


class AndOperation(ArithmeticOperation):
    def __call__(self, value, **flags):
        for v in self.values:
            value &= v
        return value

bitwise_and = AndOperation


class OrOperation(ArithmeticOperation):
    def __call__(self, value, **flags):
        for v in self.values:
            value |= v
        return value

bitwise_or = OrOperation


class XorOperation(ArithmeticOperation):
    def __call__(self, value, **flags):
        for v in self.values:
            value ^= v
        return value

xor = bitwise_xor = XorOperation


class CallOperation(Operation):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def __call__(self, value, **kwargs):
        return value(*self.args, **self.kwargs)

call = CallOperation
