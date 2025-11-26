import os
import sys

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

def main():
    os.environ['LC_ALL'] = 'C'

    try:
        with open('setup.py', 'w') as f:
            f.write("""
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

name = 'mypkg'
author = u'Lóts of åccénts Ánd diàcritičs'
author_email = u'me@myjob.org'
copyright = u'2020, ' + author

setup(name=name,
      author=author,
      author_email=author_email,
      url=r'http://',
      packages=find_packages(exclude=['doc', 'tests', 'tests.*']),
      version='0.1',
      )
""")
        import pytest
        pytest.collect([os.path.join(os.getcwd(), 'setup.py')])
    except Exception as e:
        print_stacktrace(e)
        assert False, "pytest failed to collect tests"

if __name__ == "__main__":
    main()
