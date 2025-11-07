Here is a new standalone Python file `reproducer.py` that reproduces the issue:

```python
from docutils.core import publish_string
import sys
import traceback

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
    try:
        text = r'''\documentclass{article}
\usepackage{fancyvrb}
\begin{document}
.. role:: python(code)
   :language: python
   :class: highlight

Inline :python:`def foo(1 + 2 + None + "abc"): pass` code block

.. code-block:: python

   def foo(1 + 2 + None + "abc"): pass
\end{document}'''
        output = publish_string(text, writer_name='latex')
        if b'\n ' in output or b' \n' in output:
            raise AssertionError('Expected no whitespace at start and end of inline code')
    except Exception as e:
        print_stacktrace(e)
    else:
        print('Issue not present')
        exit(0)
```

This script uses the `publish_string` function to generate LaTeX output from a given text. It checks if there is any whitespace at the start or end of the inline code block by searching for `\n ` or ` \n` in the output. If it finds any, it raises an `AssertionError`.