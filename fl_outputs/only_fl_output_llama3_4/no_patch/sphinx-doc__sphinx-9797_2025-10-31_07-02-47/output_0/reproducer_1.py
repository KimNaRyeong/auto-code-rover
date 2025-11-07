import inspect
import sys
import traceback

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

def reproduce_issue():
    try:
        import sphinx
        from sphinx.ext import autodoc
        
        class Parent:
            @classmethod
            def method(cls) -> int:
                """Return an integer."""
                return 17


        class Child(Parent):
            @classmethod
            def method(cls):
                return 42

        sphinx_app = sphinx.Application()
        sphinx_app.builder = autodoc.AutoDocumentBuilder(sphinx_app, outdir="docs")
        sphinx_app.config.autodoc_member_order = 'bysource'
        
        sphinx_app.build_all()
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue not reproduced")

if __name__ == "__main__":
    reproduce_issue()
