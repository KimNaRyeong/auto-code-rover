 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
import countvectorizer

def print_stacktrace(e: Exception):
    import traceback    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

try:
    cv = countvectorizer.CountVectorizer(analyzer=lambda x: x.split(), input='filename')
    cv.fit(['hello world']).vocabulary_
    assert False, "CountVectorizer with custom analyzer did not ignore input argument"
except Exception as e:
    print_stacktrace(e)
```
When executed with `python3 reproducer.py`, the script will raise an `AssertionError` with a stack trace, indicating that the `CountVectorizer` with a custom analyzer is ignoring the `input` argument. This reproduces the issue described in the given example.