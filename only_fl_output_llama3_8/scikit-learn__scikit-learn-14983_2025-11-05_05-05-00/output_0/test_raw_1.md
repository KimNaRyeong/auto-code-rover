The issue is not with the `RepeatedKFold` and `RepeatedStratifiedKFold` classes, but rather with the scikit-learn package itself. The error message indicates that the package has not been built correctly.

To reproduce this issue, you can try to run a simple Python script that imports scikit-learn:

```python
import sys
from sklearn import __version__

print(f"Scikit-learn version: {__version__}")
```

If the package is not installed or not built correctly, you will get an error message similar to the one you saw.