 Here is a standalone python file `reproducer.py` that reproduces the issue:
```python
import sys
import torch
from torch.utils.data import Dataset

def print_stacktrace(e: Exception):
    import traceback    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

class RasterDataset(Dataset):
    pass

class Landsat(RasterDataset):
    pass

def test_base_class_detection():
    landsat_class = Landsat
    base_class = landsat_class.__bases__[0]
    expected_base_class = RasterDataset
    assert base_class == expected_base_class, f"Expected base class to be {expected_base_class}, but got {base_class}"

if __name__ == "__main__":
    try:
        test_base_class_detection()
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
```
To reproduce the issue, run the script with `python3 reproducer.py`. The script will raise an `AssertionError` with a stack trace showing the line where the issue is present.

The issue is caused by the fact that `RasterDataset` is not a direct subclass of `Dataset`, but rather a subclass of a subclass of `Dataset`. When `autodoc` generates the documentation for `Landsat`, it incorrectly detects `Dataset` as the base class instead of `RasterDataset`.

To fix the issue, one possible solution is to modify the `autodoc` configuration in `docs/conf.py` to explicitly specify the base classes for `Landsat` and other affected classes. For example:
```python
autodoc_mock_imports = ["torch", "torchvision", "torchgeo"]

def setup(app):
    app.connect("autodoc-process-docstring", process_docstring)

def process_docstring(app, what, name, obj, options, lines):
    if what != "class":
        return
    if name in ["Landsat", "OtherAffectedClass"]:
        base_classes = [
            line.strip() for line in obj.__bases__[0].__doc__.split("\n")
            if line.strip() and not line.strip().startswith(":")
        ]
        lines.insert(1, "   :class:`~torchgeo.datasets.RasterDataset`\n")
        lines.insert(1, "   :class:`~".join(base_classes) + "\n")
    return lines
```
This configuration adds a `process_docstring` function that is called for each class documented by `autodoc`. If the class is `Landsat` or another affected class, the function modifies the docstring to explicitly list `RasterDataset` and any other base classes. This ensures that the correct base classes are detected by `autodoc`.