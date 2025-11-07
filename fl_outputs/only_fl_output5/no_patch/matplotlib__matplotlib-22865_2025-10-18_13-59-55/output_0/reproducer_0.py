import matplotlib as mpl
import numpy as np
import matplotlib.pyplot as plt  
from matplotlib.colors import from_levels_and_colors

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

def test_colorbar_edges():
    my_cmap = mpl.cm.viridis
    bounds = np.arange(10)
    nb_colors = len(bounds) + 1
    colors = my_cmap(np.linspace(100, 255, nb_colors).astype(int))
    my_cmap, my_norm = from_levels_and_colors(bounds, colors, extend='both')

    plt.figure(figsize=(5, 1))
    ax = plt.subplot(111)
    cbar = mpl.colorbar.ColorbarBase(ax, cmap=my_cmap, norm=my_norm, orientation='horizontal', drawedges=True)
    plt.subplots_adjust(left=0.05, bottom=0.4, right=0.95, top=0.9)

    # Save figure to check if edges at extremities are visible
    output_path = "colorbar_test.png"
    plt.savefig(output_path)
    plt.close()

    # Analyze saved image to assert presence of edges
    try:
        from PIL import Image
        img = Image.open(output_path)
        pixels = np.array(img)

        # Assumption: Extremities are devoid of edges if pixels on both ends
        # have no significant color difference indicating missing black lines

        # Taking arbitrary pixel rows and checking the extremities for black lines
        top_row = pixels[0, :, :].mean(axis=1)
        bottom_row = pixels[-1, :, :].mean(axis=1)

        # Asserting if extremities contain black lines (assuming a significant color difference)
        # This is a simplistic check and assumes the absence of black lines if the mean color value is consistent
        assert np.std(top_row[:5]) > 10 and np.std(bottom_row[:5]) > 10, "Edges at extremities not drawn."

    except AssertionError as e:
        print_stacktrace(e)
        raise

    except Exception as e:
        print("Unexpected error:", e)
        raise

try:
    test_colorbar_edges()
except AssertionError:
    # Exit with non-zero code to indicate failure
    import sys
    sys.exit(1)
# Exit with 0 when issue is fixed
sys.exit(0)
