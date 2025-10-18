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

def test_plt_sca_with_subfigures():
    import matplotlib.pyplot as plt

    fig = plt.figure()
    subfigs = fig.subfigures(2, 1)

    axarr = subfigs[0].subplots(2, 2)

    try:
        plt.sca(axarr[0, 0])
        print("Issue not present. `plt.sca()` worked as expected with subfigures.")
        return True
    except Exception as e:
        print_stacktrace(e)
        return False

if __name__ == "__main__":
    issue_present = not test_plt_sca_with_subfigures()
    assert issue_present, "The script did not raise an error as expected when the issue is present."
    # If the issue is present, it should have raised an error and printed a stack trace.
