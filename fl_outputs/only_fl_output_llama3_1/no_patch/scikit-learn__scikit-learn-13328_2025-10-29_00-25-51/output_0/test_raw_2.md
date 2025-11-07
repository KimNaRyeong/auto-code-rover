The issue is not with the code you provided, but rather with the way scikit-learn was installed. The error message indicates that scikit-learn has not been built correctly.

To reproduce this issue, you would need to install scikit-learn in a way that prevents it from being built correctly. This could be done by installing an older version of scikit-learn or by modifying the installation process to prevent the build step from occurring.

Here is an example of how you might modify the installation process to reproduce this issue:

```
pip install --no-build scikit-learn
```

This command will install scikit-learn without building it, which should cause the same error message that you are seeing.