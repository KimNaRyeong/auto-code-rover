import unittest
from django.utils.translation import gettext_lazy as _

def pluralize(value, forms):
    if isinstance(value, int) and value == 1:
        return forms[0]
    elif isinstance(value, str) and value.lower() == 'one':
        return forms[0]
    try:
        if len(str(value)) == 1:
            return forms[0]
    except TypeError:
        pass
    return ''

class TestPluralize(unittest.TestCase):
    def test_pluralize_error(self):
        self.assertEqual(pluralize(object, ['singular', 'plural']), 'singular')

if __name__ == '__main__':
    try:
        unittest.main()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
    else:
        exit(0)

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

