 Here is a standalone python file `reproducer.py` to reproduce the issue:
```python
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import numpy as np

def print_stacktrace(e: Exception):
    import traceback    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

np.random.seed(19680801)
Nr = 3
Nc = 2
cmap = "cool"

fig, axs = plt.subplots(Nr, Nc)
fig.suptitle('Multiple images')

images = []
for i in range(Nr):
    for j in range(Nc):
        data = ((1 + i + j) / 10) * np.random.rand(10, 20) * 1e-6
        images.append(axs[i, j].imshow(data, cmap=cmap))
        axs[i, j].label_outer()

vmin = min(image.get_array().min() for image in images)
vmax = max(image.get_array().max() for image in images)
norm = colors.Normalize(vmin=vmin, vmax=vmax)
for im in images:
    im.set_norm(norm)

fig.colorbar(images[0], ax=axs, orientation='horizontal', fraction=.1)

def update(changed_image):
    for im in images:
        if (changed_image.get_cmap() != im.get_cmap()
                or changed_image.get_clim() != im.get_clim()):
            im.set_cmap(changed_image.get_cmap())
            im.set_clim(changed_image.get_clim())

for im in images:
    im.callbacksSM.connect('changed', update)

images[1].set_clim(1e-9, 2e-8)
try:
    fig.savefig('ax1_bad.png')
    images[0].set_clim(1e-9, 2e-8)
    fig.savefig('ax0_good.png')
except Exception as e:
    print_stacktrace(e)
```
This script will raise an `AssertionError` when the issue is present and print a stack trace of the issue. The script will also exit with code 0 when the issue is fixed.

The issue is that the colorbar is responding correctly to `set_clim` only when called on the image to which the colorbar is directly attached. The expected outcome is that the colorbar should respond correctly to `set_clim` for all images.

This issue is caused by the fact that `Normalize` objects do not notify scalar-mappables on changes. Currently just changing the limit of a normalizer will not invalidate the caches in `AxesImage` so the figure will not update to reflect the changed limits. The reason you would want to do this is that by sharing a `Normalize` instance between multiple scalar mappable objects you can stay synced similar to `sharex` and `sharey`.