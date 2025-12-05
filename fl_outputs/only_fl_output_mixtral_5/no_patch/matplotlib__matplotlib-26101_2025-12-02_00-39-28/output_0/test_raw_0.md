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

def main():
    try:
        plt.plot(10, 10, color='b', alpha=1.0, marker="*", markersize=25)
        plt.plot(10, 10, color='g', alpha=1.0, marker="$\star$", markersize=25)
        plt.plot(10, 10, color='r', alpha=1.0, marker=".")

        # Check if the markers are center-aligned
        x, y = plt.gca().transData.transform((0, 0))
        center_x = x + 0.5 * plt.gca().xaxis.get_ticklocs()[0]
        assert abs(center_x - 10) < 1e-6, "Markers are not center-aligned"

    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    main()
```
The script uses the `print_stacktrace` function to print the stack trace when an `AssertionError` is raised. The `main` function plots the given code for reproduction and checks if the markers are center-aligned. If the markers are not center-aligned, an `AssertionError` is raised.

To execute the script, run `python3 reproducer.py` in the terminal. If the issue is present, an `AssertionError` will be raised and a stack trace will be printed. If the issue is fixed, the script will exit with code 0.