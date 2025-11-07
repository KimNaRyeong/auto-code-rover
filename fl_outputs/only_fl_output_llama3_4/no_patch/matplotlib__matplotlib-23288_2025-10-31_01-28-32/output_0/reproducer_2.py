import matplotlib.pyplot as plt
from io import BytesIO
import unittest
from PIL import Image, ImageDraw
import os
import sys
import traceback

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

class Reproducer(unittest.TestCase):

    def test_bug(self):
        try:
            plt.text(0.5, 0.5, "Long text with link", rotation=45, url="https://matplotlib.org")
            buf = BytesIO()
            plt.savefig(buf, format='pdf')
            if not os.path.exists('link.pdf'):
                raise AssertionError("The link area is not rotated")

        except AssertionError as e:
            print_stacktrace(e)
            sys.exit(1)

if __name__ == '__main__':
    unittest.main()
