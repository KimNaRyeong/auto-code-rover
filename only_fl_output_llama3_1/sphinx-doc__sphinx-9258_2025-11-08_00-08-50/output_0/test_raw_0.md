Here is the reproducer script:

```python
def foo(text: bytes | str):
    """Bar

    :param text: a text
    :type text: bytes | str

    """
    pass

if __name__ == "__main__":
    try:
        foo(b"Hello")
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

```

This script defines the `foo` function with type hinting that accepts both `bytes` and `str`. Then, it calls this function with a `bytes` argument. If the issue is present (i.e., Python does not support union types), an `AssertionError` will be raised, which will be caught by the script and printed to the console along with the stack trace.