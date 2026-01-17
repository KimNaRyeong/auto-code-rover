# reproducer.py
import traceback
import sys

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def custom_min(x):
    import numpy as np
    return float(np.asarray(x).min())

def main():
    try:
        import seaborn as sns
        tips = sns.load_dataset("tips")
        ax = sns.pointplot(x="day", y="tip", data=tips, estimator=custom_min)
    except TypeError as e:
        # The specific issue we're looking for.
        print_stacktrace(e)
    except Exception as e:
        # Any other exceptions will be treated as a failure to reproduce.
        print_stacktrace(e)
        raise AssertionError("The script failed due to an unexpected exception.")

if __name__ == "__main__":
    main()
