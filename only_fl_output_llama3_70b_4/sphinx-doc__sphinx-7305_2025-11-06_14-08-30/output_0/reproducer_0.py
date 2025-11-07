import sys
from docutils.parsers.rst import Directive, directives
from docutils.parsers.rst.directives import flag

def print_stacktrace(e: Exception):
    import traceback
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

class MyDirective(Directive):
    has_content = False
    required_arguments = 0
    optional_arguments = 0

    def run(self):
        pass

directives.register_directive('mydirective', MyDirective)

try:
    from docutils.parsers.rst import Parser
    parser = Parser()
    parser.parse(".. py:method:: f(*, a=2**4)\n.. py:method:: g(a=2**4)")
except Exception as e:
    print_stacktrace(e)
    assert False, "Could not parse arglist"
else:
    sys.exit(0)
