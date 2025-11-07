```python
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

def assert_marker_alignment():
    from matplotlib import pyplot as plt
    import numpy as np

    # Create a sample plot
    fig, ax = plt.subplots()
    normal_marker, = ax.plot(10, 10, color='b', alpha=1.0, marker="*", markersize=25, label='Normal star')
    mathtext_marker, = ax.plot(10, 10, color='g', alpha=1.0, marker="$\star$", markersize=25, label='Mathtext star')
    reference_marker, = ax.plot(10, 10, color='r', alpha=1.0, marker=".", markersize=25, label='Reference dot')

    # Ensure the figure is drawn to access updated properties
    plt.draw()

    # Get marker positions
    normal_marker_x, normal_marker_y = normal_marker.get_data()
    mathtext_marker_x, mathtext_marker_y = mathtext_marker.get_data()
    reference_marker_x, reference_marker_y = reference_marker.get_data()

    # Calculate the difference in marker alignment
    alignment_error = np.abs(mathtext_marker_y - reference_marker_y) + np.abs(mathtext_marker_x - reference_marker_x)
    
    assert alignment_error < 1e-9, "Mathtext markers are not center-aligned with reference markers."

if __name__ == "__main__":
    try:
        assert_marker_alignment()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
    else:
        print("Success: The mathtext markers are center-aligned with reference markers.")
        exit(0)
```