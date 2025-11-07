Here is the reproducer script:

```python
import os
import subprocess
import unittest
from tempfile import TemporaryDirectory

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

class TestPylintIssue(unittest.TestCase):
    def test_pylint_issue(self):
        with TemporaryDirectory() as tmpdir:
            os.makedirs(os.path.join(tmpdir, '.a'))
            foo_path = os.path.join(tmpdir, '.a', 'foo.py')
            bar_path = os.path.join(tmpdir, 'bar.py')

            with open(foo_path, 'w') as f:
                f.write('# import re\n')

            with open(bar_path, 'w') as f:
                f.write('# import re\n')

            process = subprocess.run(['pylint', '--recursive=y', '.'], capture_output=True, text=True)
            output = process.stdout

            self.assertIn('C0104: Disallowed name "foo" (disallowed-name)', output)
            self.assertIn('C0114: Missing module docstring (missing-module-docstring)', output)
            self.assertIn('W0611: Unused import re (unused-import)', output)

            process = subprocess.run(['pylint', '--recursive=y', '--ignore=.a', '.'], capture_output=True, text=True)
            output = process.stdout

            self.assertNotIn('C0104: Disallowed name "foo" (disallowed-name)', output)
            self.assertNotIn('C0114: Missing module docstring (missing-module-docstring)', output)
            self.assertNotIn('W0611: Unused import re (unused-import)', output)

            process = subprocess.run(['pylint', '--recursive=y', '--ignore-patterns="^\.a"', '.'], capture_output=True, text=True)
            output = process.stdout

            self.assertNotIn('C0104: Disallowed name "foo" (disallowed-name)', output)
            self.assertNotIn('C0114: Missing module docstring (missing-module-docstring)', output)
            self.assertNotIn('W0611: Unused import re (unused-import)', output)

        if process.stdout:
            raise AssertionError("Pylint does not respect ignores in --recursive=y mode")

    def test_pylint_issue_fails(self):
        try:
            self.test_pylint_issue()
        except AssertionError as e:
            print_stacktrace(e)
            exit(1)
        else:
            exit(0)


if __name__ == '__main__':
    unittest.main()
```

This script creates a temporary directory and two files (`foo.py` and `bar.py`) inside it. It then runs Pylint in different modes (with and without ignore settings) and checks the output for the expected issues. If any of these commands do not produce the expected results, an `AssertionError` is raised with the stack trace printed using the provided function.