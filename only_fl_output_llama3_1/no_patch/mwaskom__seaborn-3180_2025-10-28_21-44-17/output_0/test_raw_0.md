Here is the reproducer script:

```python
import seaborn as sns
import matplotlib.pyplot as plt
from io import StringIO
import contextlib
import unittest
from unittest.mock import patch

@contextlib.contextmanager
def captured_output():
    new_stdout = StringIO()
    old_stdout = sys.stdout
    try:
        sys.stdout = new_stdout
        yield new_stdout
    finally:
        sys.stdout = old_stdout


class TestIssue(unittest.TestCase):

    def test_issue(self):
        with self.assertRaises(AssertionError) as e:
            # Your code to reproduce the issue here
            import seaborn as sns

            sns.set_context("paper")
            sns.set_style("white")

            data = (sns.load_dataset('iris').set_index('species')*1e7).reset_index()
            g = sns.relplot(data=data, x='sepal_length', y='sepal_width', col='species', 
                            col_wrap=2, height=2.5)
            g.set_titles(row_template="{row_name}", col_template="SOMEWHATLONG-{col_name}")
            for axes in g.axes.flat:
                axes.ticklabel_format(axis='both', style='scientific', scilimits=(0, 0))

        print_stacktrace(e)

if __name__ == '__main__':
    unittest.main()
```

This script will run the test case and if the issue is present, it will raise an `AssertionError` with a stack trace.