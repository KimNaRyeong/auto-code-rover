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

def check_images_similarity(img1, img2):
    from PIL import Image
    import numpy as np

    im1 = np.array(Image.open(img1))
    im2 = np.array(Image.open(img2))

    return np.array_equal(im1, im2)

def reproduce_issue():
    import matplotlib
    import matplotlib.pyplot as plt
    import numpy as np

    arr = np.arange(100).reshape((10, 10))

    matplotlib.rcParams['figure.constrained_layout.use'] = True

    fig, ax_dict = plt.subplot_mosaic('AB;AC', figsize=(6,9), width_ratios=[3,2],
                                      layout='compressed')

    for key in ["B", "C"]:
        ax_dict[key].imshow(arr)

    fig.savefig("test1.png", bbox_inches="tight")
    fig.savefig("test2.png", bbox_inches="tight")

    if not check_images_similarity("test1.png", "test2.png"):
        raise AssertionError("The images saved in two instances are not identical.")

if __name__ == "__main__":
    try:
        reproduce_issue()
    except AssertionError as e:
        print_stacktrace(e)
```

In this script, `reproduce_issue` tries to reproduce the issue as per the given bug report. It saves two figures under the assumption that some specific configurations might lead to the figures being different upon inspection, contrary to user expectations. The `check_images_similarity` function loads these images and checks if they are exactly the same.

Please note: This script compares the images on a pixel-by-pixel basis, which might not always capture differences visible to human eyes, especially when differences are small or nuanced (such as slight changes in layout or color). Additionally, factors like font rendering differences across environments could potentially influence this comparison. 

The script concludes with an `AssertionError` if the images are found not to be identical, along with a traceback pointing to where the check failed, thereby indicating the presence of the reported issue. If the images are identical, it implies the issue might be resolved or not reproducible under these specific test conditions, and the script would exit with code 0.