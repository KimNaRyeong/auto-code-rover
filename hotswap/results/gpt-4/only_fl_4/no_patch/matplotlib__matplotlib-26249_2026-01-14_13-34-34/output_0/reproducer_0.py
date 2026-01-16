# reproducer.py

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

def run_reproducer():
    try:
        import numpy as np
        from matplotlib import pylab as plt

        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')
        ax.scatter([1, np.nan, 3], [2, np.nan, 4], [3, np.nan, 5], color=[[.5, .5, .5, .5]]*3, s=11.5)
        
        # If execution reaches this point without exception, the issue is considered fixed.
        return True
    except ValueError as e:
        print_stacktrace(e)
        return False

def main():
    assert not run_reproducer(), "The issue is still present."

if __name__ == "__main__":
    main()
