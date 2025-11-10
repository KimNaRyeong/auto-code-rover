I apologize for the previous mistake. Here is a new reproducer script that should reproduce the issue:

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

        wrapper_exception = Exception()
        wrapper_exception.__cause__ = wrapper_exception
        try:
            raise WrapperException() from wrapper_exception
        except WrapperException as exc:
            for frame in get_traceback_frames(exc):
                pass

    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == "__main__":
    main()
```

This script should reproduce the issue by creating a cause/context cycle and then entering an infinite loop when trying to extract traceback frames.