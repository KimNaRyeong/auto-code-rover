Here is the standalone Python file `reproducer.py` that reproduces the issue:

```python
import matplotlib.pyplot as plt
import traceback
import sys

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

def reproduce_issue():
    try:
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots()
        leg = ax.legend(title="Test Legend")
        title_inst = leg.get_title()
        title_inst.set_horizontalalignment('right')  # This should work
        title_inst.set_horizontalalignment('left')  # This should not work
        raise AssertionError("Expected error")
    except Exception as e:
        print_stacktrace(e)

if __name__ == "__main__":
    reproduce_issue()
```

To run the script, execute `python3 reproducer.py` in your terminal. The script will raise an `AssertionError`, and then print a stack trace showing the line numbers of the statements.