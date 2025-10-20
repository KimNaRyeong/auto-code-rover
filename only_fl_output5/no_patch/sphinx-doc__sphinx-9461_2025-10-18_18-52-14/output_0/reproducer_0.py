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

class ClassMethodProperty:
    @classmethod
    @property
    def test_prop(cls):
        """Documented class property"""
        return "value"

def reproduction_test():
    # Test if the property is documented
    try:
        doc = ClassMethodProperty.test_prop.__doc__
        assert doc is not None, "Class method property is not documented"
        assert doc == "Documented class property", "Documentation does not match"
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
    except Exception as e:
        print_stacktrace(e)
        exit(1)
    
    print("Test passed. Issue is resolved.")
    exit(0)

if __name__ == "__main__":
    reproduction_test()
