Here is the reproducer script:

```python
import os
from django.core.management import call_command
from django.conf import settings
from django.contrib.staticfiles.storage import ManifestStaticFilesStorage
import unittest
from unittest.mock import patch, mock_open
from io import StringIO
from contextlib import redirect_stdout
from django.utils.log import logger

class MyManifestStaticFilesStorage(ManifestStaticFilesStorage):
    max_post_process_passes = 0

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

class TestReproducer(unittest.TestCase):
    @patch('builtins.open', new_callable=mock_open, read_data='')
    def test_reproduce(self, mock_file):
        settings.STATICFILES_STORAGE = "MyManifestStaticFilesStorage"
        with redirect_stdout(StringIO()):
            try:
                call_command('collectstatic')
            except Exception as e:
                print_stacktrace(e)
                self.fail("Expected AssertionError")
        else:
            print("Test passed")

if __name__ == '__main__':
    unittest.main()
```

This script sets up a test case that attempts to run the `collectstatic` command with the custom storage class. If an exception is raised, it prints the stack trace and fails the test.