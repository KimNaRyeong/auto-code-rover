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

def test_issue():
    class BaseClass:
        @classmethod
        @property
        def baseclass_property(cls):
            """Base class property."""
            return "baseclass"

    try:
        import sphinx
        from sphinx.ext import autodoc
        autodoc.generate_doc(BaseClass)
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue not fixed")

if __name__ == "__main__":
    test_issue()
