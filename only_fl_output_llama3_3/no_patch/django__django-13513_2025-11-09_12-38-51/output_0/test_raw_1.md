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

def test_issue():
    class TestView:
        def get(self, request):
            try:
                raise RuntimeError('my error')
            except Exception as exc:
                raise ValueError('my new error') from None

    view = TestView()
    try:
        view.get(None)
    except (ValueError, AssertionError) as e:
        print_stacktrace(e)
        assert False, "Issue not present"

test_issue()
```

This script will reproduce the issue by defining a class `TestView` that raises an exception and then catching it. The script will raise an `AssertionError` if the issue is not present, which means the debug error view still shows the original `RuntimeError`.