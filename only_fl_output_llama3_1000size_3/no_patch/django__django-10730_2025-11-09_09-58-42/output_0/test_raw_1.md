Here is the reproducer script:

```python
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

def main():
    try:
        def get_traceback_frames(exc_value):
            while exc_value:
                yield from traceback.extract_tb(exc_value.__traceback__)
                if exc_value.__cause__':
                    exc_value = exc_value.__cause__
                else:
                    raise AssertionError("Expected cause/context cycle")

        except_wrapper_exception = Exception()
        exc_value = except_wrapper_exception
        for frame in get_traceback_frames(exc_value):
            pass

    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == "__main__":
    main()
```

When you run this script with `python3 reproducer.py`, it should reproduce the issue and raise an `AssertionError` when the cause/context cycle is detected.