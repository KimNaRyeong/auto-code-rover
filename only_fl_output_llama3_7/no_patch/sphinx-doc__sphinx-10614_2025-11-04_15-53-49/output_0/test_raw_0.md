Here is a standalone Python script to reproduce the issue:

```python
import sphinx
from sphinx.ext import inheritance_diagram
from sphinx.application import SphinxApplication
from sphinx.builders import Builder
from sphinx.util import logging
import os
import sys
import shutil
import tempfile
import unittest

class Reproducer(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.src_dir = os.path.join(self.temp_dir, 'docs_source')
        self.build_dir = os.path.join(self.temp_dir, 'docs_build')

        os.makedirs(self.src_dir)
        os.makedirs(self.build_dir)

        shutil.copytree('path_to_your_project', self.src_dir)

    def test_reproducer(self):
        app = SphinxApplication()
        builder = Builder(app, 'html')
        builder.config.master_doc = 'index'
        builder.config.inheritance_diagram_module_name = 'my_package'

        try:
            builder.build_all()
        except AssertionError as e:
            print_stacktrace(e)
            self.fail("Expected no exception")

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

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

if __name__ == '__main__':
    unittest.main()
```

This script will create a temporary directory, copy your project files to it, and then run the Sphinx build process. If the issue is present, it will raise an `AssertionError` and print the stack trace.