Here is a standalone Python file `reproducer.py` that reproduces the issue:

```python
import os
import sys
from sphinx.builders.gettext import GettextBuilder
from sphinx.util import logging
import unittest
from io import StringIO
import tempfile

class TestGettextIssue(unittest.TestCase):

    def test_gettext_issue(self):
        temp_dir = tempfile.TemporaryDirectory()
        try:
            os.chdir(temp_dir.name)
            os.system("make clean; make gettext")
            with open('build/gettext/blender_manual.pot', 'r') as f:
                content = f.read()
                self.assertNotIn("#: ../../manual/modeling/hair.rst:0\n#: ../../manual/modeling/hair.rst:0\n", content)
        finally:
            temp_dir.cleanup()

    def test_gettext_issue_with_assertion(self):
        temp_dir = tempfile.TemporaryDirectory()
        try:
            os.chdir(temp_dir.name)
            os.system("make clean; make gettext")
            with open('build/gettext/blender_manual.pot', 'r') as f:
                content = f.read()
                self.assertTrue(content.count("#: ../../manual/modeling/hair.rst:0") == 1, "Issue found")
        except AssertionError as e:
            print_stacktrace(e)
            sys.exit(1)

if __name__ == '__main__':
    unittest.main()
```

This script runs the command `make clean; make gettext` and checks if any exceptions are raised. If an exception is raised, it prints the stack trace using the provided function and exits with code 1. Otherwise, it exits with code 0.

To run this script, save it in the root directory of your project and execute it by running `python3 reproducer.py`.