import json

from nodes import Var, Function, Call, Let, Str, Int, Bool, If, Binary, Tuple, First, Second, Print, File
from utils import identity, with_parameters, with_parameter

SUPPORTED_NODES = {
    Var.kind: (Var, identity),
    Function.kind: (Function, with_parameters),
    Call.kind: (Call, identity),
    Let.kind: (Let, with_parameter),
    Str.kind: (Str, identity),
    Int.kind: (Int, identity),
    Bool.kind: (Bool, identity),
    If.kind: (If, identity),
    Binary.kind: (Binary, identity),
    Tuple.kind: (Tuple, identity),
    First.kind: (First, identity),
    Second.kind: (Second, identity),
    Print.kind: (Print, identity),
}


def to_ast_node(object_data: dict):
    if kind := object_data.get("kind"):
        if node_handler := SUPPORTED_NODES.get(kind):
            node, handler = node_handler
            node_arguments = handler(object_data)

            return node(**node_arguments)

    return object_data


if __name__ == "__main__":
    with open("./source.rinha.json") as file:  # @todo mudar path
        data = json.load(file, object_hook=to_ast_node)

        file = File(**data)
        file.expression.execute()
