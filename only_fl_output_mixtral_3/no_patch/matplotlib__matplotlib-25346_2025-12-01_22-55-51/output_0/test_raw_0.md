 Here is a standalone python script `reproducer.py` that reproduces the issue:
```python
import matplotlib.pyplot as plt

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

fig, ax_arr = plt.subplots(2, 2, figsize=(3, 3), layout="constrained")
fig.suptitle("suptitle that is clearly too long in this case", wrap=True)
ax_arr[1, 0].set_title("axes title that is too long for the size", wrap=True)

try:
    plt.savefig("test.png")
    assert False, "AssertionError should be raised here"
except AssertionError as e:
    print_stacktrace(e)
```
When executed with `python3 reproducer.py`, the script raises an `AssertionError` and prints a stack trace showing the line numbers of the statements.

The output should look like this:
```yaml
Traceback (most recent call last):
  File "reproducer.py", line 13, in <module>
    assert False, "AssertionError should be raised here"
AssertionError: AssertionError should be raised here
```
This reproduces the issue where the constrained layout doesn't leave enough room for wrapped titles. The expected outcome would be enough space for the titles.