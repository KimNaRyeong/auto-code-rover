import matplotlib.pyplot as plt
import sys
import traceback

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

try:
    fig = plt.figure()
    subfigs = fig.subfigures(2, 2, wspace=0.5, hspace=0.5)  
    for i, subfig in enumerate(subfigs.flat):
        ax = subfig.subplots()
        ax.plot([1, 2])
    
    # Check if the figure is rendered correctly
    fig.tight_layout(pad=0)
    assert fig.get_figwidth() > 8, "wspace and hspace are not set correctly"

except AssertionError as e:
    print_stacktrace(e)
    sys.exit(1)

sys.exit(0)
