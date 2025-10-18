import ast
import traceback
import sys

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

class ImportChecker(ast.NodeVisitor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.imports = {}
        self.used = set()

    def visit_Import(self, node):
        for alias in node.names:
            self.imports[alias.name] = node.lineno
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        for alias in node.names:
            self.imports[alias.name] = node.lineno
        self.generic_visit(node)

    def visit_Name(self, node):
        if node.id in self.imports:
            self.used.add(node.id)
        self.generic_visit(node)

    def check_unused_imports(self):
        unused_imports = set(self.imports.keys()) - self.used
        if unused_imports:
            raise AssertionError(f"Unused imports detected: {', '.join(unused_imports)}")

def main():
    test_code = """
\"\"\"Docstring.\"\"\"

import abc
from abc import ABC

X = ...  # type: abc.ABC
Y = ...  # type: ABC
"""
    try:
        tree = ast.parse(test_code)
        checker = ImportChecker()
        checker.visit(tree)
        checker.check_unused_imports()
        print("No issue detected.")
    except Exception as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    main()
