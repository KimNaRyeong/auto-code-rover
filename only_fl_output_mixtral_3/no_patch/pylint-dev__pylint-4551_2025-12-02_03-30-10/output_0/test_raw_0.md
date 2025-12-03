 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
import pyreverse
import sys
from typing import Optional

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

class C:
    def __init__(self, a: str = None):
        self.a = a

def main():
    pyreverse.pyreverse(".", stdout=sys.stdout)

if __name__ == "__main__":
    try:
        main()
    except AssertionError:
        e = sys.exc_info()[1]
        print_stacktrace(e)
        sys.exit(1)
```
To reproduce the issue, run the script with `python3 reproducer.py`. The output should show the current behavior of `pyreverse` without reading Python type hints:
```css
Traceback (most recent call last):
  File "reproducer.py", line 28, in <module>
    main()
  File "reproducer.py", line 24, in main
    pyreverse.pyreverse(".", stdout=sys.stdout)
  File "/usr/local/lib/python3.8/dist-packages/pyreverse/__init__.py", line 192, in pyreverse
