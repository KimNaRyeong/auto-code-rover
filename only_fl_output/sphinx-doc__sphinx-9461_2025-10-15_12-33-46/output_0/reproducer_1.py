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

class DemoClass:
    _class_property_value = "Example"
    
    @classmethod
    @property
    def class_property(cls):
        """This is a class property docstring."""
        return cls._class_property_value

try:
    # Check if the class property docstring is accessible in the expected way
    docstring = DemoClass.class_property.__doc__
    if docstring is None:
        raise AssertionError("Class property docstring is not accessible")
    else:
        print(f"Docstring found: {docstring}")

    # Python 3.10 introduction check
    if hasattr(DemoClass.class_property, '__wrapped__'):
        print(f"Method supports '__wrapped__' attribute, indicating Python >= 3.10 behavior.")
    else:
        raise AssertionError("Expected '__wrapped__' attribute not found, indicating potential issue with Python < 3.10 or Sphinx documentation generation.")

except Exception as e:
    print_stacktrace(e)
    exit(1)  # Exit with an error code signaling the issue is reproduced or there is an unexpected failure

print('Documentation extraction behavior for class properties seems to work as expected.')
exit(0)  # Exit with a success code signaling no reproduction of the issue
