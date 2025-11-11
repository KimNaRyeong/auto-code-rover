The issue you're experiencing is not related to the `xr.polyval` function, but rather with a NumPy version issue. The error message indicates that `np.unicode_` was removed in the NumPy 2.0 release and you should use `np.str_` instead.

Here's an example of how you can reproduce this issue:

```Python
import numpy as np

try:
    print(np.unicode_)
except AttributeError as e:
    print_stacktrace(e)
    raise AssertionError("Expected np.unicode_ to exist")
```

This script will try to print `np.unicode_`. If the NumPy version is 2.0 or higher, it should raise an exception and print a stack trace.

To fix this issue, you can either upgrade your NumPy version to one that supports `np.unicode_`, or use `np.str_` instead.