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

class MyClass:
    @classmethod
    @property
    def my_property(cls):
        """This is the MyClass my_property documentation."""
        return 'This is my_property'

def main():
    try:
        # Directly checking if the documentation can be fetched as Sphinx would.
        doc = MyClass.my_property.__doc__
        assert doc == "This is the MyClass my_property documentation.", \
            "Failed to access the expected documentation string."
        
        print("Success, documentation was correctly retrieved:", doc)
        
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)  # Indicating failure due to AssertionError

    except Exception as e:
        print_stacktrace(e)
        exit(1)  # Indicating failure due to unexpected errors

if __name__ == "__main__":
    main()
    exit(0)  # Indicating success when no error is raised
