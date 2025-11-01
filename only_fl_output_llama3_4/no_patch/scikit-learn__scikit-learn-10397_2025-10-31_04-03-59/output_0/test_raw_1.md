The issue is not with the RidgeCV class itself, but rather with the installation of scikit-learn. The error message indicates that scikit-learn has not been built correctly.

To reproduce this issue, you would need to install scikit-learn from source and then try to run a script that imports RidgeCV. However, since the issue is with the installation of scikit-learn, it's not possible to write a standalone reproducer script for this specific error.

Here is an example of how you might reproduce this issue:

1. Clone the scikit-learn repository from GitHub.
2. Navigate to the cloned repository and run `python setup.py install` or `make` in the source directory.
3. Once scikit-learn has been installed, try running a script that imports RidgeCV, such as the following:
```
from sklearn.linear_model import RidgeCV
print("RidgeCV imported successfully")
```
If you still encounter the error after installing scikit-learn correctly, then it's likely due to an issue with your Python environment or operating system.