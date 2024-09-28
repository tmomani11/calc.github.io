from lark import Lark, Transformer
import math
import sys

grammar = """
?start: expr

# Expression rules for addition and subtraction
?expr: expr "+" term     -> add
     | expr "-" term     -> sub
     | term

# Term rules for multiplication and division
?term: term "*" factor   -> mul
     | term "/" factor   -> div
     | factor

# Factor rules for exponentiation
?factor: factor "^" atom        -> pow
       | atom

# Atom rules for negation, parentheses, and log
?atom: "log" expr "base" expr -> log
     | "-" atom               -> neg
     | "(" expr ")"
     | NUMBER

%import common.NUMBER
%import common.WS
%ignore WS
"""

# Define the parser using Lark
parser = Lark(grammar, parser='lalr')


# Transformer class to evaluate the AST
class CalculateTree(Transformer):

    def log(self, args):
        return self._to_int_if_possible(math.log(args[0], args[1]))

    def add(self, args):
        return self._to_int_if_possible(args[0] + args[1])

    def sub(self, args):
        return self._to_int_if_possible(args[0] - args[1])

    def mul(self, args):
        return self._to_int_if_possible(args[0] * args[1])

    def div(self, args):
        return self._to_int_if_possible(args[0] / args[1])

    def pow(self, args):
        return self._to_int_if_possible(args[0] ** args[1])

    def neg(self, args):
        return self._to_int_if_possible(-args[0])

    def NUMBER(self, token):
        return float(token)

    def _to_int_if_possible(self, value):
        # Convert float to int if it's a whole number (e.g., 2.0 becomes 2)
        if isinstance(value, float) and value.is_integer():
            return int(value)
        return value


# Function to evaluate the expression
def evaluate_expression(expression):
    # Parse the input expression using Lark parser
    tree = parser.parse(expression)

    # Transform the AST and calculate the result
    calc_tree = CalculateTree()
    result = calc_tree.transform(tree)

    return result


if __name__ == '__main__':
    # Take the expression as a command-line argument
    if len(sys.argv) != 2:
        print("Usage: python calculator_cfg.py <expression>")
        sys.exit(1)

    expression = sys.argv[1]
    try:
        result = evaluate_expression(expression)
        print(result)
    except Exception as e:
        print(f"Error evaluating expression: {e}")
