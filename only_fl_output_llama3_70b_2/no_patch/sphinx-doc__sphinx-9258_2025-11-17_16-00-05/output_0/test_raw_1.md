Here is the `reproducer.py` file to reproduce the issue:
```
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

def foo(text):
    """Bar

    :param text: a text
    :type text: bytes | str

    """
    pass

try:
    import inspect
    signature = inspect.signature(foo)
    parameter = signature.parameters['text']
    assert 'bytes | str' in str(parameter.annotation), "Union type not supported"
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

exit(0)
```
This script defines a function `foo` with a docstring that specifies the type of the `text` parameter as `bytes | str`. It then uses the `inspect` module to get the signature of the function and checks if the annotation of the `text` parameter contains the string "bytes | str". If it doesn't, an `AssertionError` is raised, and the script prints the stack trace using the provided `print_stacktrace` function.