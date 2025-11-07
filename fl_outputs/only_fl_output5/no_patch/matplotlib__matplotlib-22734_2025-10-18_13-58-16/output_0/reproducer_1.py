import numpy as np
import matplotlib.pyplot as plt
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

def test_tripcolor_clim_behavior():
    # Generate some random data
    x = np.random.rand(100)
    y = np.random.rand(100)
    z = np.random.rand(100)

    # Create a tripcolor plot with defined clim
    fig, ax = plt.subplots()
    tpc = ax.tripcolor(x, y, z, clim=(0, 0.5))
    plt.colorbar(tpc)

    # Check if tripcolor honored the clim
    # Unfortunately, directly checking the clim of tripcolor doesn't straightforwardly indicate 
    # whether the issue exists because the API does set the clim,
    # but the visual representation might still ignore it.
    # Therefore, we need a different approach to effectively reproduce the issue:
    # One approach is to compare the color range directly if such data is accessible
    # or use a heuristic that an incorrect clim affects the output range noticeably.
    # For our reproducer, we'll inspect the limits in a more indirect manner:
    
    try:
        # Fetch the colors used in the collection and verify if they respect the clim
        colors = tpc.get_facecolors()  # This gets the RGBA values used in the plot
        # Assuming the issue causes colors to map outside the clim range [0, 0.5],
        # we would expect colors that correspond to values outside this range.
        # We simplistically check if the max color value (ignoring the alpha) exceeds a threshold
        max_color_intensity = colors[:, :3].max()
        expected_max_intensity = plt.cm.viridis(0.5)[0]  # Assuming viridis as the colormap and fetching intensity for 0.5 value
        
        assert max_color_intensity <= expected_max_intensity + 0.01, "Color intensity exceeds expected range due to clim being ignored."
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)  # Use a non-zero exit code to indicate failure

    print("Test passed successfully.")
    sys.exit(0)  # Exiting with code 0 when the issue is fixed

if __name__ == "__main__":
    test_tripcolor_clim_behavior()
