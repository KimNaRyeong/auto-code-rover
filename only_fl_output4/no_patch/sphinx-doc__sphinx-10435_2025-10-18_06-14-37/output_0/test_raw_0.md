```python
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

def test_inline_code_highlighting():
    from sphinx.application import Sphinx
    import os

    # Create minimal Sphinx project layout
    srcdir = '_test_inline_code_highlighting_src'
    os.makedirs(srcdir, exist_ok=True)
    with open(os.path.join(srcdir, 'conf.py'), 'w') as f:
        f.write(
            '''
import sys, os
sys.path.append(os.path.abspath('.'))

extensions = []

project = 'Test Inline Code Whitespace Sphinx'
master_doc = 'index'
            '''
        )
    with open(os.path.join(srcdir, 'index.rst'), 'w') as f:
        f.write(
            '''
.. role:: python(code)
   :language: python
   :class: highlight

Inline :python:`def foo(1 + 2 + None + "abc"): pass` code block

.. code-block:: python

   def foo(1 + 2 + None + "abc"): pass
            '''
        )

    # Build with Sphinx
    outdir = os.path.join(srcdir, '_build', 'latex')
    doctreedir = os.path.join(srcdir, '_build', 'doctrees')
    sphinx = Sphinx(
        srcdir, srcdir, outdir, doctreedir, 'latexpdf',
        {},  # No additional options
    )
    sphinx.build()

    # Verify the output
    latex_file_path = os.path.join(outdir, f"{sphinx.config.project}.tex")
    with open(latex_file_path, 'r') as f:
        content = f.read()
        assert r"\sphinxcode{\sphinxupquote{%" in content, "Inline code block doesn't contain expected LaTeX markup at the start."
        assert r"%}}" in content, "Inline code block doesn't contain expected LaTeX markup at the end."

try:
    test_inline_code_highlighting()
except AssertionError as e:
    print_stacktrace(e)
    raise SystemExit(1)
else:
    print("The issue is not present.")

```

This script sets up a minimal Sphinx project programmatically, simulates the issue as described, and then checks the generated `.tex` file for the expected corrected output (i.e., no unwanted whitespace around inline code blocks).

Upon running `python3 reproducer.py` in your project's root directory:

- If the issue is present, the script will print a stack trace pointing to where the assertion failed and exit with status code `1`, indicating an error.
- If the issue is not present (i.e., Sphinx behaves as expected and includes the correct LaTeX markup for inline code highlighting without adding unwanted whitespace), the script will print "The issue is not present." and exit with status code `0`, indicating success.

Make sure Sphinx is installed in your environment before running the script.