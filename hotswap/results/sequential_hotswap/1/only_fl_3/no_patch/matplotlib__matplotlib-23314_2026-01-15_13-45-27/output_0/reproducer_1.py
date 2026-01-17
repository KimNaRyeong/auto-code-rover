# reproducer.py
import sys

def print_stacktrace(e: Exception):
    import traceback
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def check_subplot_visibility():
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D  # This import registers the 3D projection, but is not directly used

    try:
        # Create a figure with 3D subplots
        fig, (ax1, ax2) = plt.subplots(1, 2, subplot_kw={'projection': '3d'})
        ax1.scatter(1, 1, 1)
        ax2.scatter(1, 1, 1, c='r')

        # Attempt to make the first ax invisible
        ax1.set_visible(False)

        # Force a draw of the figure; this might be necessary to propagate visibility changes
        plt.draw()

        # Check if any artists in ax1 are still visible
        # This iterates over collections, lines, patches, and texts in ax1:
        for artist in ax1.collections + ax1.lines + ax1.patches + ax1.texts:
            if artist.get_visible():
                raise AssertionError("Subplot ax1 still contains visible artists, but it should be completely invisible.")

        # If no AssertionError is raised, assume visibility handling works as expected.
        print("The issue regarding subplot visibility cannot be reproduced with this method.")
        sys.exit(0)

    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == "__main__":
    check_subplot_visibility()
