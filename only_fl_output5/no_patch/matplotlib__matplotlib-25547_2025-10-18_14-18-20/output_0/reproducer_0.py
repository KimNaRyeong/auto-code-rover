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

def test_nan_colors_issue():
    import numpy as np
    import matplotlib.pyplot as plt
    import warnings

    def run_with_partial_nan():
        c = np.full(10, np.nan)
        c[0] = 1.0
        plt.scatter(np.ones(10), np.ones(10), c=c)
        plt.show()

    def run_with_all_nan():
        plt.scatter(np.ones(10), np.ones(10), c=np.full(10, np.nan))
        plt.show()

    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        run_with_partial_nan()
        assert not w, "Expected no warnings for partial NaN colors"

    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        run_with_all_nan()
        if not w:
            raise AssertionError("Expected a warning for all NaN colors")

def test_errorbar_nan_issue():
    import matplotlib.pyplot as plt
    import numpy as np
    
    fig, ax = plt.subplots(1, 1)
    try:
        ax.errorbar([0], [0], yerr=[np.nan])
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("The errorbar plot with all-nan yerr should not raise an exception") from e

def main():
    try:
        test_nan_colors_issue()
        test_errorbar_nan_issue()
        print("All tests passed successfully.")
    except AssertionError as ae:
        print_stacktrace(ae)
        raise

if __name__ == "__main__":
    main()
