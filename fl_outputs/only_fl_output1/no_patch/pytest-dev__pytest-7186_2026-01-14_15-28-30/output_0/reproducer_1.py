import subprocess
import os

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

def reproduce_issue():
    setup_py_content = '''
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

name = 'mypkg'
author = u'Lóts of åccénts Ánd diàcritičs'
author_email = u'me@myjob.org'

setup(name=name,
      author=author,
      author_email=author_email,
      url=r'http://',
      packages=find_packages(exclude=['doc', 'tests', 'tests.*']),
      version='0.1',
      )
'''

    # Write setup.py file with UTF-8 content
    with open('setup.py', 'w', encoding='utf-8') as f:
        f.write(setup_py_content)

    # Set C locale
    os.environ['LC_ALL'] = 'C'

    # Attempt to run pytest with setup.py
    try:
        result = subprocess.run(['pytest', 'setup.py'], capture_output=True, text=True)
        # If UnicodeDecodeError is mentioned in stderr, the issue has been reproduced
        if "UnicodeDecodeError" in result.stderr:
            print("Issue reproduced successfully: UnicodeDecodeError encountered as expected.")
        else:
            assert False, "Expected UnicodeDecodeError was not encountered."
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Error during the reproduction attempt") from e

if __name__ == "__main__":
    try:
        reproduce_issue()
    except AssertionError as error:
        print(f"AssertionError: {error}")
        exit(1)  # Exiting with non-zero to indicate failure/reproduction of the issue
    else:
        print("No issue detected. Exiting with code 0.")
        exit(0)
