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

def check_images_identical(img1_path, img2_path):
    from PIL import Image
    from PIL import ImageChops
    img1 = Image.open(img1_path)
    img2 = Image.open(img2_path)
    diff = ImageChops.difference(img1, img2)
    if diff.getbbox():
        raise AssertionError("Images are not identical")

def main():
    import matplotlib
    import matplotlib.pyplot as plt
    import numpy as np

    arr = np.arange(100).reshape((10, 10))

    matplotlib.rcParams['figure.constrained_layout.use'] = True

    fig, ax_dict = plt.subplot_mosaic('AB;AC', figsize=(6, 9), width_ratios=[3, 2],
                                      layout='compressed')

    for key in ["B", "C"]:
        ax_dict[key].imshow(arr)
    
    fig.savefig("test1.png", bbox_inches="tight")
    fig.savefig("test2.png", bbox_inches="tight")

    try:
        check_images_identical("test1.png", "test2.png")
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    try:
        main()
    except AssertionError:
        exit(1)
    exit(0)
```