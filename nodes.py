from enum import Enum
import binary_operations


class Location:
    start: int
    end: int
    filename: str


class Var:
    kind: str = "Var"
    text: str
    location: Location

    def __init__(self, text: str, **kwargs):
        self.text = text

    def execute(self, **kwargs):
        return kwargs.get("namespace", {}).get(self.text)


class Parameter:
    text: str
    location: Location

    def __init__(self, text: str, **kwargs):
        self.text = text


class Function:
    kind: str = "Function"
    parameters: list[Parameter]
    value: "Term"
    location: Location

    def __init__(self, parameters: list[Parameter], value: "Term", **kwargs):
        self.parameters = parameters
        self.value = value

    def execute(self, **kwargs):
        parameters = list(map(lambda parameter: parameter.text, self.parameters))
        total_parameters = len(parameters)

        def function(*args, **function_kwargs):
            total_arguments = len(args)

            if total_arguments != total_parameters:
                raise Exception(f"Expected {total_parameters} arguments, got {total_arguments}")

            global_namespace = function_kwargs.get("namespace", {})
            function_namespace = dict(zip(parameters, args))

            namespace = {**global_namespace, **function_namespace}

            return self.value.execute(namespace=namespace)

        return function


class Call:
    kind: str = "Call"
    callee: "Term"
    arguments: list["Term"]
    location: Location

    def __init__(self, callee: "Term", arguments: list["Term"], **kwargs):
        self.callee = callee
        self.arguments = arguments

    def execute(self, **kwargs):
        arguments = list(map(lambda argument: argument.execute(**kwargs), self.arguments))

        return self.callee.execute(**kwargs)(*arguments, **kwargs)


class Let:
    kind: str = "Let"
    name: Parameter
    value: "Term"
    next: "Term"
    location: Location

    def __init__(self, name: Parameter, value: "Term", **kwargs):
        self.name = name
        self.value = value
        self.next: "Term" = kwargs["next"]  # to avoid shadowing the built-in `next` function

    def execute(self, **kwargs):
        global_namespace = kwargs.get("namespace", {})
        local_namespace = {self.name.text: self.value.execute(**kwargs)}
        namespace = {**global_namespace, **local_namespace}

        return self.next.execute(namespace=namespace)


class Str:
    kind: str = "Str"
    value: str
    location: Location

    def __init__(self, value: str, **kwargs):
        self.value = value

    def execute(self, **kwargs):
        return str(self.value)


class Int:
    kind: str = "Int"
    value: int
    location: Location

    def __init__(self, value: int, **kwargs):
        self.value = value

    def execute(self, **kwargs):
        return int(self.value)


class BinaryOp(Enum):
    Add = binary_operations.add
    Sub = binary_operations.sub
    Mul = binary_operations.mul
    Div = binary_operations.div
    Rem = binary_operations.rem
    Eq = binary_operations.eq
    Neq = binary_operations.neq
    Lt = binary_operations.lt
    Gt = binary_operations.gt
    Lte = binary_operations.lte
    Gte = binary_operations.gte
    And = binary_operations.and_
    Or = binary_operations.or_


class Bool:
    kind: str = "Bool"
    value: bool
    location: Location

    def __init__(self, value: bool, location: Location, **kwargs):
        self.value = value
        self.location = location

    def execute(self, **kwargs):
        pass


class If:
    kind: str = "If"
    condition: "Term"
    then: "Term"
    otherwise: "Term"
    location: Location

    def __init__(self, condition: "Term", then: "Term", otherwise: "Term", **kwargs):
        self.condition = condition
        self.then = then
        self.otherwise = otherwise

    def execute(self, **kwargs):
        if self.condition.execute(**kwargs):
            return self.then.execute(**kwargs)

        return self.otherwise.execute(**kwargs)


class Binary:
    kind: str = "Binary"
    lhs: "Term"
    op: BinaryOp
    rhs: "Term"
    location: Location

    def __init__(self, lhs: "Term", op: BinaryOp, rhs: "Term", **kwargs):
        self.lhs = lhs
        self.op = op
        self.rhs = rhs

    def execute(self, **kwargs):
        operator = getattr(BinaryOp, self.op)
        left = self.lhs.execute(**kwargs)
        right = self.rhs.execute(**kwargs)

        return operator(left, right)


class Tuple:
    kind: str = "Tuple"
    first: "Term"
    second: "Term"
    location: Location

    def __init__(self, first: "Term", second: "Term", **kwargs):
        self.first = first
        self.second = second

    def execute(self, **kwargs):
        pass


class First:
    kind: str = "First"
    value: "Term"
    location: Location

    def __init__(self, value: "Term", **kwargs):
        self.value = value

    def execute(self, **kwargs):
        pass


class Second:
    kind: str = "Second"
    value: "Term"
    location: Location

    def __init__(self, value: "Term", **kwargs):
        self.value = value

    def execute(self, **kwargs):
        pass


class Print:
    kind: str = "Print"
    value: "Term"
    location: Location

    def __init__(self, value: "Term", **kwargs):
        self.value = value

    def execute(self, **kwargs):
        print(self.value.execute(**kwargs))


class File:
    name: str = "File"
    expression: "Term"
    location: Location

    def __init__(self, expression: "Term", **kwargs):
        self.expression = expression

    def execute(self, **kwargs):
        return self.expression.execute()


Term = Var | Function | Call | Let | Str | Int | Bool | If | Binary | Tuple | First | Second | Print
