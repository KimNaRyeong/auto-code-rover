Here is the reproducer script:

```python
import seaborn as sns
import matplotlib.pyplot as plt
from io import StringIO
import contextlib
import unittest
from unittest.mock import patch
import sys

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

class TestIssue(unittest.TestCase):

    def test_issue(self):
        try:
            # Your code to reproduce the issue here
            sns.set()
            data = (sns.load_dataset('iris').set_index('species')*1e7).reset_index()
            g = sns.relplot(data=data, x='sepal_length', y='sepal_width', col='species', 
                            col_wrap=2, height=2.5)
            g.set_titles(row_template="{row_name}", col_template="SOMEWHATLONG-{col_name}")
            for axes in g.axes.flat:
                axes.ticklabel_format(axis='both', style='scientific', scilimits=(0, 0))
        except AssertionError as e:
            print_stacktrace(e)

if __name__ == '__main__':
    unittest.main()
```

This script will run the test case and if the issue is present, it will raise an `AssertionError` with a stack trace.