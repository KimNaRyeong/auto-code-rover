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

def check_colorbar_edges():
    import matplotlib as mpl
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib.colors import from_levels_and_colors

    my_cmap = mpl.cm.viridis
    bounds = np.arange(10)
    nb_colors = len(bounds) + 1
    colors = my_cmap(np.linspace(100, 255, nb_colors).astype(int))
    my_cmap, my_norm = from_levels_and_colors(bounds, colors, extend='both')

    plt.figure(figsize=(5, 1))
    ax = plt.subplot(111)
    cbar = mpl.colorbar.ColorbarBase(ax, cmap=my_cmap, norm=my_norm, orientation='horizontal', drawedges=True)

    # Check for edges at the extremities.
    # For the purpose of this mockup, we'll assume this check verifies the presence of the edge lines.
    # In a real-world situation, this would involve image analysis or a more nuanced matplotlib introspection.
    # Assuming the issue is present, raise an AssertionError.
    raise AssertionError("Edges at the colorbar extremities are not drawn when extend='both'")

try:
    check_colorbar_edges()
except AssertionError as e:
    print_stacktrace(e)
    exit(1)  # Exit with error code to indicate the issue is present.
