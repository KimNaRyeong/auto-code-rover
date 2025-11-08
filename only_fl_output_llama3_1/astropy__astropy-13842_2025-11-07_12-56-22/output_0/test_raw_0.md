Here is the reproducer script:

```python
import astropy.table as at
import unittest
from io import StringIO
from contextlib import redirect_stdout

class TestIssue(unittest.TestCase):

    def test_issue(self):
        table1 = at.QTable({
            'foo': [1, 2, 3],
            'bar': [4, 5, 6],
            'baz': [7, 8, 9]
        })

        print(table1.colnames)
        table2 = at.QTable({
            "new": table1["foo"],
            "name": table1["bar"]
        }, copy=False)
        print(table1.colnames)

        if table1.colnames != ['foo', 'bar', 'baz']:
            f = StringIO()
            with redirect_stdout(f):
                raise AssertionError("Column names in original table changed")
            self.fail(f.getvalue())

if __name__ == '__main__':
    unittest.main(exit=False)
```

This script creates the same tables as in your example, checks if the column names of `table1` have changed after creating `table2`, and raises an `AssertionError` with a stack trace if they have.