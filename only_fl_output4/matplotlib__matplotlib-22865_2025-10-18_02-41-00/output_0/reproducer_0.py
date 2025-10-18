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

if __name__ == "__main__":
    try:
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
    
        plt.subplots_adjust(left=0.05, bottom=0.4, right=0.95, top=0.9)
        plt.draw()
        
        # Check if edges at extremities are drawn for extend='both'
        # Extracting the drawn patches (edges) in the colorbar
        edges = [child for child in cbar.ax.get_children() if isinstance(child, mpl.patches.Rectangle)]
        # There should be more edges than just the number of bounds if edges at extremities are drawn properly
        expected_edge_count = len(bounds) + 1  # Considering an extra edge for each extension
        actual_edge_count = len(edges)
    
        # Raising AssertionError if the actual edge count is not as expected
        if actual_edge_count <= expected_edge_count:
            raise AssertionError("Edges at extremities are not drawn when extend='both' and drawedges=True.")
    
        print("Issue not found. The expected outcome is met.")
    
    except Exception as e:
        print_stacktrace(e)
        exit(1)  # Exit with error code if an exception is caught

    exit(0)  # Exit with success code if no issue is found
