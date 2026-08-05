import ast
import logging


def get_node_type_names(code):
    syntax_tree = ast.parse(code)
    return {type(node).__name__ for node in ast.walk(syntax_tree)}


def check_structural_requirements(code, required=None, disallowed=None):
    node_types_present = get_node_type_names(code)
    errors = []
    if disallowed is not None:
        for node_name in disallowed:
            if node_name in node_types_present:
                errors.append("Your solution should not use a " + node_name + " statement")
    if required is not None:
        for node_name in required:
            if node_name not in node_types_present:
                errors.append("Your solution should use a " + node_name + " statement")
    return errors
