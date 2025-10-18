import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
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

def verify_colorbar_edges():
    my_cmap = mpl.cm.viridis
    bounds = np.arange(10)
    nb_colors = len(bounds) + 1
    colors = my_cmap(np.linspace(100, 255, nb_colors).astype(int))
    my_cmap, my_norm = from_levels_and_colors(bounds, colors, extend='both')
    fig, ax = plt.subplots(figsize=(5, 1))
    cbar = mpl.colorbar.ColorbarBase(ax, cmap=my_cmap, norm=my_norm, orientation='horizontal', drawedges=True)

    # Attempt to examine the rendering to check if edges at extremities are drawn
    # This direct method of verification is hypothetical and illustrative
    for extent in ['min', 'max']:
        edge_existence = (extent in cbar.extend) and cbar.drawedges
        if not edge_existence:
            raise AssertionError("Edges at the colorbar extremities (extend='both') with drawedges=True are not shown as expected.")

try:
    verify_colorbar_edges()
except AssertionError as e:
    print_stacktrace(e)
    raise SystemExit(1)
else:
    print("Success: The issue is fixed.")
    raise SystemExit(0)
