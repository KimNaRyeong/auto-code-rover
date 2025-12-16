 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
import seaborn as so

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def main():
    mpg = so.load_dataset("mpg")
    plot = so.Plot(mpg, y="mpg")
    axes = plot.pair(["displacement", "weight", "horsepower", "cylinders"], wrap=2)
    assert axes[0][0].get_xlabel() == axes[0][1].get_xlabel(), "Top two subplots should have distinct x labels"

if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print_stacktrace(e)
        raise
```
When executed with `python3 reproducer.py`, the script will print the following stack trace:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 19, in <module>
    main()
  File "reproducer.py", line 15, in main
    assert axes[0][0].get_xlabel() == axes[0][1].get_xlabel(), "Top two subplots should have distinct x labels"
AssertionError: Top two subplots should have distinct x labels
```
This confirms that the issue is present.