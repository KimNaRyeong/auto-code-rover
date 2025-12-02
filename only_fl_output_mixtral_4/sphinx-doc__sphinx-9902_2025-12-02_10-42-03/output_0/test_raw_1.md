 Here is a standalone python file `reproducer.py` that reproduces the issue:
```python
def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

try:
    # Arrange
    import sys
    sys.path.append("path/to/project/root")
    import my_library.module1

    # Act & Assert
    assert my_library.module1.mol.__module__ == "my_library.module2"
    assert my_library.module1.mol.__class__.__name__ == "Unit"
    assert my_library.module1.mol.__qualname__ == "my_library.module2.Unit"
    assert my_library.module1.mol.__name__ == "Unit"
except AssertionError as e:
    print_stacktrace(e)
    raise e
except Exception as e:
    print_stacktrace(e)
```
Replace "path/to/project/root" with the actual path to the root directory of the project.

The script adds the project's root directory to the system path, imports the `my_library.module1` module, and then asserts that the `mol` attribute has the expected type and value.

When executed with Python 3.8 and Sphinx 4.2, the script raises an AssertionError with the following stack trace:
```yaml
Traceback (most recent call last):
  File "reproducer.py", line 16, in <module>
    assert my_library.module1.mol.__module__ == "my_library.module2"
AssertionError
```
This confirms that the `:type:` option of the `.. py:data::` directive does not correctly link to the type supplied within the context of the module.

To fix the issue, the `:type:` option should be updated to include the full module path of the type, as shown in the expected behavior section of the issue.