Here is a standalone Python file `reproducer.py` that reproduces the issue:

```python
import os
import subprocess
from unittest import TestCase

class Reproducer(TestCase):
    def test_reproduce_issue(self):
        # Run pylint with --jobs=2 and capture its output
        jobs_2_output = subprocess.check_output([
            'pylint',
            '--jobs=2',
            '--rcfile=' + os.path.join(os.getcwd(), 'pylintrc'),
            'app/codein',
            'app/melange',
            'app/soc',
            'app/summerofcode',
            'app/settings.py',
            'app/urls.py',
            'app/main.py',
            'tests/pavement.py',
            'setup.py'
        ], universal_newlines=True)

        # Run pylint with --jobs=1 and capture its output
        jobs_1_output = subprocess.check_output([
            'pylint',
            '--jobs=1',
            '--rcfile=' + os.path.join(os.getcwd(), 'pylintrc'),
            'app/codein',
            'app/melange',
            'app/soc',
            'app/summerofcode',
            'app/settings.py',
            'app/urls.py',
            'app/main.py',
            'tests/pavement.py',
            'setup.py'
        ], universal_newlines=True)

        # Check if the outputs are different
        self.assertNotEqual(jobs_2_output, jobs_1_output,
                             "Expected different output for --jobs=1 and --jobs=2")

    def test_no_issue(self):
        # Run pylint with --jobs=2 and capture its output
        jobs_2_output = subprocess.check_output([
            'pylint',
            '--jobs=2',
            '--rcfile=' + os.path.join(os.getcwd(), 'pylintrc'),
            'app/codein',
            'app/melange',
            'app/soc',
            'app/summerofcode',
            'app/settings.py',
            'app/urls.py',
            'app/main.py',
            'tests/pavement.py',
            'setup.py'
        ], universal_newlines=True)

        # Run pylint with --jobs=1 and capture its output
        jobs_1_output = subprocess.check_output([
            'pylint',
            '--jobs=1',
            '--rcfile=' + os.path.join(os.getcwd(), 'pylintrc'),
            'app/codein',
            'app/melange',
            'app/soc',
            'app/summerofcode',
            'app/settings.py',
            'app/urls.py',
            'app/main.py',
            'tests/pavement.py',
            'setup.py'
        ], universal_newlines=True)

        # Check if the outputs are the same
        self.assertEqual(jobs_2_output, jobs_1_output,
                         "Expected same output for --jobs=1 and --jobs=2")

if __name__ == '__main__':
    try:
        Reproducer().test_reproduce_issue()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

    try:
        Reproducer().test_no_issue()
    except AssertionError as e:
        print_stacktrace(e)
        exit(0)
```

This script runs pylint with both --jobs=2 and --jobs=1, captures the output, and then checks if the outputs are different. If they are, it raises an `AssertionError` and prints a stack trace using the provided function.