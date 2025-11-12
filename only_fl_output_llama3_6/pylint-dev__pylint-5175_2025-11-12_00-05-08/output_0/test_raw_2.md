Here is the reproducer script:

```python
def function(file, *args, sep=";"):
    """Description of the function

    Parameters
    ----------
    file : str
        Path to the input.
    *args
        Relevant parameters.
    sep : str, optional
        File separator.
    """
    pass

print_stacktrace(AssertionError("Expected no warning"))

```

This script should reproduce the issue by raising an `AssertionError` and printing a stack trace.