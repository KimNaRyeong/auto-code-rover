import sphinx
from docutils import nodes
from docutils.parsers.rst import Directive

def print_stacktrace(e: Exception):
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

def rst_directive(app, docname):
    app.builder.get_target_url('example_python_function')

def setup(app):
    app.connect("source-file-translate", rst_directive)

try:
    from sphinx.domains.python import PythonDomain
    domain = PythonDomain()
    domain.register_function('example_python_function')
    print(f"Fragment identifier: {domain.get_qualified_id('example_python_function')}")
except Exception as e:
    print_stacktrace(e)
    raise AssertionError("Expected behavior not observed")

if __name__ == "__main__":
    setup(None)
