import docutils
from docutils.parsers.rst import Directive, roles
from docutils.parsers.rst.directives import unchanged

def test():
    """test tests something.
    """

def reproducer():
    doc = "\n".join([".. default-role:: cmsreference", "", test.__doc__])
    try:
        directives = {'default-role': unchanged}
        roles.register_canonical_role('cmsreference', 'cmsreference')
        pub = docutils.core.Publisher()
        pub.set_writer('html')
        docutils.core.publish_string(doc, publisher=pub)
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Error rendering view docstring")

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

if __name__ == "__main__":
    reproducer()
