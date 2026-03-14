"""Built-in tools and tool registry for day-15 project."""

import ast
import operator
from typing import Callable


def calculator(expression: str) -> str:
    """Evaluates a basic arithmetic expression and returns the result as a string."""
    allowed_ops = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.USub: operator.neg,
    }

    def _eval(node: ast.AST) -> float:
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in allowed_ops:
            return allowed_ops[type(node.op)](_eval(node.left), _eval(node.right))
        if isinstance(node, ast.UnaryOp) and type(node.op) in allowed_ops:
            return allowed_ops[type(node.op)](_eval(node.operand))
        raise ValueError(f"Unsupported expression: {ast.dump(node)}")

    try:
        tree = ast.parse(expression.strip(), mode="eval")
        result = _eval(tree.body)
        return str(result)
    except Exception as e:
        return f"Error: {e}"


def word_count(text: str) -> str:
    """Returns the number of words in the given text as a string."""
    count = len(text.split())
    return str(count)


def reverse_string(text: str) -> str:
    """Returns the reversed version of the given string."""
    return text[::-1]


TOOL_REGISTRY: dict[str, Callable[[str], str]] = {
    "calculator": calculator,
    "word_count": word_count,
    "reverse_string": reverse_string,
}
