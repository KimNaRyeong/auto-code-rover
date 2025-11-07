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

try:
    from matplotlib import colors, pyplot as plt, cm
    import numpy as np

    def reproduce_issue():
        Nr, Nc = 3, 2
        fig, axs = plt.subplots(Nr, Nc)
        images = []

        for i in range(Nr):
            for j in range(Nc):
                data = np.random.rand(10, 20)
                images.append(axs[i, j].imshow(data, cmap='viridis', norm=colors.Normalize(vmin=0, vmax=1)))

        # Add colorbar for the first image object
        cbar = fig.colorbar(images[0], ax=axs.ravel().tolist())

        # Manually change the clim for one of the other images
        original_clim = images[1].get_clim()
        images[1].set_clim(0.1, 0.9)  # Change clim
        changed_clim = images[1].get_clim()

        # Check whether the colorbar reflects this change
        colorbar_clim = cbar.mappable.get_clim()
        if not (colorbar_clim[0] == changed_clim[0] and colorbar_clim[1] == changed_clim[1]):
            raise AssertionError("Colorbar limits do not reflect the changed clim of the image.")

    reproduce_issue()
except AssertionError as e:
    print_stacktrace(e)
    exit(1)  # Exit with error code when the issue is present
except Exception as e:
    print_stacktrace(e)
    exit(1)

print("The issue appears to be fixed.")
exit(0)
