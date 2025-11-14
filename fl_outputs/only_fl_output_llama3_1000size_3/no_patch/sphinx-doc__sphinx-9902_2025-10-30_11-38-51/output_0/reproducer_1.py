from docutils import nodes, utils
from docutils.parsers.rst import Directive

def setup(app):
    app.connect('doctree-resolved', on_doctree_resolved)

def on_doctree_resolved(app, doctree):
    for node in doctree.traverse(nodes.directive):
        if node.hasattr('hasoption') and node.getoption('type'):
            type_option = node.getoption('type')
            if not isinstance(type_option, str) or not type_option.startswith('my_library.module2.'):
                raise AssertionError("Expected :type: option to be a fully qualified name")

def print_stacktrace(e):
    import traceback
    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

if __name__ == '__main__':
    try:
        setup(None)  # This should raise an AssertionError
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
