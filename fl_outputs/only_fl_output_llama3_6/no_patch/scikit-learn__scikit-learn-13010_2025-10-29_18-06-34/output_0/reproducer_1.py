import numpy as np

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

try:
    sample = np.full([10_000_000, 1], 10.0, dtype=np.float16)
    from sklearn.preprocessing import StandardScaler
    StandardScaler().fit_transform(sample)
except Exception as e:
    print_stacktrace(e)
    assert False, "Expected the issue to be fixed"
