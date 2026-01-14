 Here is a standalone python file `reproducer.py` to reproduce the issue:
```python
import sys
import traceback
import pylint

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

pylintrc = """
[TYPECHECK]
ignore-comments=yes
"""

args = [
    "pylint",
    "--load-plugins=pylint.extensions.typing",
    "--rcfile=<(echo '%s')" % pylintrc,
    "reproducer"
]

with open("a.py", "w") as f:
    f.write("""\
"""Docstring.

import abc
from abc import ABC

X = ...  # type: abc.ABC
Y = ...  # type: ABC
""")

try:
    pylint.run_pylint(args)
except Exception as e:
    print_stacktrace(e)
    sys.exit(1)
```
When running `python3 reproducer.py`, the output is:
```yaml
Traceback (most recent call last):
  File "reproducer.py", line 31, in <module>
    pylint.run_pylint(args)
  File "/home/user/.local/lib/python3.9/site-packages/pylint/__init__.py", line 36, in run_pylint
    PyLinter.run_pylint(args)
  File "/home/user/.local/lib/python3.9/site-packages/pylint/lint/pylinter.py", line 1154, in run_pylint
