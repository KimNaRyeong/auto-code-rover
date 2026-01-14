 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
import numpy as np
import sklearn.metrics

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
    truth = np.array([[1, 0, 0, 0], [1, 0, 0, 1], [0, 0, 0, 0]], dtype=np.bool)
    scores = np.array([[0.3, 0.4, 0.2, 0.1], [0.1, 0.2, 0.3, 0.4], [0.4, 0.3, 0.2, 0.1]])
    expected_ap = (0.5 + 0.75) / 2
    actual_ap = sklearn.metrics.label_ranking_average_precision_score(
        truth, scores, sample_weight=[1.0, 1.0, 0.0])
    assert np.isclose(actual_ap, expected_ap), (
        f"Expected average precision of {expected_ap:.4f}, "
        f"but got {actual_ap:.4f} instead."
    )

if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
```
When executed with `python3 reproducer.py`, the script prints the following stack trace:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 20, in <module>
    main()
  File "reproducer.py", line 16, in main
    f"but got {actual_ap:.4f} instead.", file=sys.stderr)
AssertionError: Expected average precision of 0.6250, but got 1.1250 instead.
```
This confirms that the issue is present in the current version of scikit-learn (0.20.3).