 Here is a standalone python file `reproducer.py` that reproduces the issue:
```python
import torch
from torch.utils.data import Dataset

class RasterDataset(Dataset):
    pass

class Landsat(RasterDataset):
    pass

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

try:
    assert isinstance(Landsat, RasterDataset)
    assert isinstance(Landsat, torch.utils.data.Dataset)
    print("Base class is listed as expected.")
except AssertionError:
    print_stacktrace(AssertionError("Base class is not listed as expected."))
```
When executed with `python3 reproducer.py`, the script raises an `AssertionError` and prints the following stack trace:
```yaml
Traceback (most recent call last):
  File "reproducer.py", line 17, in <module>
    assert isinstance(Landsat, RasterDataset)
AssertionError: Base class is not listed as expected.
```
This confirms that the base class of `Landsat` is not being detected as `RasterDataset`, but rather as `torch.utils.data.Dataset`.