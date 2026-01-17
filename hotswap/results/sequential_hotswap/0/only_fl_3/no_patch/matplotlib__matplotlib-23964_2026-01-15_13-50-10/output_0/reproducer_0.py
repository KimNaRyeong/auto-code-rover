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

def test_matplotlib_backend_ps_issue():
    from matplotlib.figure import Figure
    try:
        figure = Figure()
        ax = figure.add_subplot(111)
        ax.annotate(text='\nLower label', xy=(0, 0))
        figure.savefig('figure.eps')
        print("Issue not present, saved figure.eps successfully.")
        return True
    except TypeError as e:
        print_stacktrace(e)
        return False

if __name__ == "__main__":
    issue_present = not test_matplotlib_backend_ps_issue()
    assert issue_present, "Expected a TypeError due to the matplotlib backend_ps issue, but it did not occur."
