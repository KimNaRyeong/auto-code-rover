import numpy as np

def reproduce_issue():
    try:
        x = np.random.choice(['a', 'b'], size=20)
        from sklearn.metrics.cluster import mutual_info_score
        mutual_info_score(x, x)
    except Exception as e:
        print_stacktrace(e)
        assert False, "Expected ValueError"

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

if __name__ == "__main__":
    reproduce_issue()
