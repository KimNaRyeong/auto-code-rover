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


class A:
    _class_property = "property"

    @classmethod
    @property
    def class_property(cls):
        """Some class property doc."""
        return cls._class_property


def check_documentation():
    expected_doc = "Some class property doc."
    actual_doc = A.class_property.__doc__

    assert actual_doc == expected_doc, f"Expected documentation '{expected_doc}' but got '{actual_doc}'."


def main():
    try:
        check_documentation()
        print("Issue fixed. Exiting with code 0.")
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)


if __name__ == "__main__":
    main()
