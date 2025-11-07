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

def assert_marker_alignment_corrected():
    from matplotlib import pyplot as plt
    import numpy as np

    fig, ax = plt.subplots()
    # Use raw string for math text to avoid escape sequence warning
    mathtext_marker, = ax.plot(0, 0, color='g', alpha=1.0, marker=r"$\star$", markersize=25, label='Mathtext star')
    normal_marker, = ax.plot(1, 0, color='b', alpha=1.0, marker="*", markersize=25, label='Normal star')

    plt.draw()

    renderer = fig.canvas.get_renderer()
    normal_marker_bbox = normal_marker.get_window_extent(renderer)
    mathtext_marker_bbox = mathtext_marker.get_window_extent(renderer)
    
    # Calculate alignment offset
    offset = np.abs(normal_marker_bbox.x0 - mathtext_marker_bbox.x0) + np.abs(normal_marker_bbox.y0 - mathtext_marker_bbox.y0)
    
    assert offset == 0, f"Mathtext markers are not properly center-aligned; offset found: {offset}"

if __name__ == "__main__":
    try:
        assert_marker_alignment_corrected()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
    except Exception as e:
        print("Unexpected error occurred.")
        print_stacktrace(e)
        exit(1)
    else:
        print("Success: The mathtext markers are properly center-aligned with normal markers.")
        exit(0)
