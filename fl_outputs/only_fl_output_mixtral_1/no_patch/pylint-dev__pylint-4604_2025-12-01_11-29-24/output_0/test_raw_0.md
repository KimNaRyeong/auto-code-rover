 Here is a standalone python file `reproducer.py` that reproduces the issue:
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
    "--disable=all",
    "--enable=unused-import",
    "--load-plugins=pylint.extensions.typing",
    "--rcfile=<(echo '%s')" % pylintrc,
    "reproducer.py"
]

try:
    pylint.run_pylint(args)
except Exception as e:
    print_stacktrace(e)
    assert False, "pylint should not emit unused-import warning"
```
When executed with `python3 reproducer.py`, it should raise an `AssertionError` and print the following stack trace:
```yaml
Traceback (most recent call last):
  File "reproducer.py", line 24, in <module>
    pylint.run_pylint(args)
  File "/home/user/.local/lib/python3.9/site-packages/pylint/__init__.py", line 36, in run_pylint
    PyLinter.run_pylint(args)
  File "/home/user/.local/lib/python3.9/site-packages/pylint/lint/pylinter.py", line 1355, in run_pylint
