import os
import sys
from django.core.management import execute_from_command_line
import subprocess
import time
import unittest
from io import StringIO
import tempfile

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

    def test_reproduce_issue(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            os.chdir(tmpdir)
            try:
                subprocess.run(['django-admin', 'startproject', 'django-test'])
                subprocess.run(['python', 'manage.py', 'runserver'])
                time.sleep(1)  # wait for the server to start
                response = subprocess.check_output(['curl', '-iX', 'HEAD', 'http://127.0.0.1:8000/'], universal_newlines=True)
                self.assertNotEqual(response, '<!DOCTYPE html>\n<html lang="en"><head>\n <meta http-equiv="content-type" content="text/html; charset=utf-8">\n <meta name="robots" content="NONE,NOARCHIVE"><title>Welcome to Django</title>\n...')
            except subprocess.CalledProcessError as e:
                print_stacktrace(e)
                self.fail()
            except Exception as e:
                print_stacktrace(e)
                self.fail()

if __name__ == '__main__':
    unittest.main()
