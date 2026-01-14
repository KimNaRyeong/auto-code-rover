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

def check_marker_alignment():
    try:
        import matplotlib.pyplot as plt
        import numpy as np
        import matplotlib.transforms as mtransforms

        # Prepare a figure
        fig, ax = plt.subplots()
        ax.set_xlim([0, 20])
        ax.set_ylim([0, 20])

        # Standard star marker
        standard_marker, = ax.plot(10, 10, marker="*", markersize=25, linestyle='None')

        # Mathtext marker
        mathtext_marker, = ax.plot(15, 10, marker=r"$\star$", markersize=25, linestyle='None', color='r')

        # Draw the figure to access the rendered positions
        fig.canvas.draw()

        # Get the data-to-display transform
        transform = ax.transData

        # Get the display coordinates for standard and mathtext markers
        standard_display = transform.transform(standard_marker.get_data())
        mathtext_display = transform.transform(mathtext_marker.get_data())

        # Assuming alignment issues will significantly offset the markers, let's define a threshold
        alignment_threshold = 1.0  # in display units, arbitrarily chosen for demonstration

        # Calculate the distance between the two markers in display space
        distance = np.linalg.norm(np.array(standard_display) - np.array(mathtext_display))

        assert distance <= alignment_threshold, f"Markers are misaligned by more than {alignment_threshold} display units."

    except AssertionError as e:
        print_stacktrace(e)
        exit(1)  # AssertionError indicates the issue is present
    except Exception as e:
        print_stacktrace(e)
        exit(2)  # Any other exception is unexpected
    else:
        print("Markers appear to be aligned within the defined threshold.")
        exit(0)

if __name__ == "__main__":
    check_marker_alignment()
