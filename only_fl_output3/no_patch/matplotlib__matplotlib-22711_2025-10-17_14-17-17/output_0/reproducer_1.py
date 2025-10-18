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

def main():
    try:
        import numpy as np
        import matplotlib.pyplot as plt
        from matplotlib.widgets import RangeSlider

        # Generate a fake image
        np.random.seed(19680801)
        N = 128
        img = np.random.randn(N, N)

        fig, axs = plt.subplots(1, 2, figsize=(10, 5))
        fig.subplots_adjust(bottom=0.25)

        # Create the RangeSlider
        slider_ax = fig.add_axes([0.20, 0.1, 0.60, 0.03])
        
        # Intentionally set to values known to cause the IndexError if the bug exists
        slider = RangeSlider(slider_ax, "Threshold", img.min(), img.max(), valinit=[img.min(), img.max()])

        # If initialization passes without IndexError, an AssertionError is raised indicating the success.
        assert False, f"Expected IndexError was not raised. Issue might have been fixed."

    except IndexError as e:
        print("IndexError caught as expected. The issue is present.")
        print_stacktrace(e)
        exit(1)  # Exit with error code to indicate the failure due to the issue being present.

    except Exception as e:
        print("An unexpected exception occurred.")
        print_stacktrace(e)
        exit(1)  # Exit with error code to indicate an unexpected failure.

if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print(e)
        exit(0)  # Exit with code 0 to indicate the issue is fixed or not reproduced.
