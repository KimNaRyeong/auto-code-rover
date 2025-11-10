import matplotlib.pyplot as plt
import matplotlib.rcsetup as rc

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

plt.rcParams['figure.autolayout'] = True
fig, axes = plt.subplots(ncols=2)
fig.tight_layout(w_pad=10)

# Check if the padding is applied correctly by checking the figure width
import matplotlib as mpl
fig_width_in = fig.get_figwidth()
assert fig_width_in > 8, "Tight layout kwargs have no effect"

exit(0)
