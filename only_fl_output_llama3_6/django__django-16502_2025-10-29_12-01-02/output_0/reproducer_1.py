import os
import sys
from django.core.management import execute_from_command_line
import subprocess
import time
import unittest
from io import StringIO

class TestReproducer(unittest.TestCase):

    def test_reproduce_issue(self):
        try:
            with open('manage.py', 'w') as f:
                f.write('from django.core.management.commands.runserver import main\nmain()')
            process = subprocess.Popen(['python3', 'manage.py', 'runserver'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, error = process.communicate(timeout=10)
            self.assertEqual(process.returncode, 0, "Expected return code 0 but got {}".format(process.returncode))
            if not output:
                output = b''
            if not error:
                error = b''
            with StringIO(output.decode('utf-8')) as out_file:
                with StringIO(error.decode('utf-8')) as err_file:
                    self.assertNotContains(out_file.getvalue(), '<!DOCTYPE html>', "Expected no HTML response but got {}".format(out_file.getvalue()))
        except Exception as e:
            print_stacktrace(e)
            self.fail("Test failed")

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

if __name__ == "__main__":
    unittest.main()
