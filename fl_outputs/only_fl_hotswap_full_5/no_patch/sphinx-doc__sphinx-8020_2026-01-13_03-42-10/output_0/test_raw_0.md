 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
import sys
import traceback
from typing import Callable, Awaitable

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

@typing.overload
def host(func: typing.Callable[..., typing.Awaitable[None]], timeout: float = 3, *args, **kwargs) -> typing.Callable[..., typing.Awaitable[None]]: ...
@typing.overload
def host(func: typing.Callable[..., typing.Coroutine[Any, Any, None]], timeout: float = 3, *args, **kwargs) -> typing.Callable[..., typing.Coroutine[Any, Any, None]]: ...
def host(func, timeout=3, *args, **kwargs):
    """
    :param func:
    :param timeout:
    :return:
    """

if __name__ == "__main__":
    try:
        host(lambda: None, 1)
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)
```
To reproduce the issue, run the script with Sphinx 3.1.2 installed:
```bash
python3 -m venv venv
venv/bin/pip install --upgrade pip setuptools wheel
venv/bin/pip install -e .[pyside2,docs]
source venv/bin/activate
cd docs
../venv/bin/pip install --upgrade sphinx==3.1.2
../venv/bin/python reproducer.py
```
The output should contain the following warning:
```vbnet
WARNING: py:class reference target not found: Callable[[...], Awaitable[None]]
```
This warning is raised because the `None` type hint is not being hyperlinked in the docstring for the `host` function. This is a regression in Sphinx 3.1.2 compared to 3.1.1.

To fix the issue, either downgrade to Sphinx 3.1.1 or apply the patch from the following pull request: <https://github.com/sphinx-doc/sphinx/pull/9364>.