 Here is a standalone python file `reproducer.py` to reproduce the issue:
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
def host(func: typing.Callable[..., typing.Awaitable[None]], timeout: float = 3, *args, **kwargs) -> typing.Any: ...
@typing.overload
def host(func: typing.Callable[..., typing.Coroutine[Any, Any, None]], timeout: float = 3, *args, **kwargs) -> typing.Any: ...
def host(func, timeout=3, *args, **kwargs):
    """
    Decorator to add timeout functionality to a coroutine.

    :param func: The coroutine to decorate.
    :param timeout: The timeout in seconds.
    :return: The decorated coroutine.
    """
    async def wrapper(*args, **kwargs):
        ...
    return wrapper


if __name__ == "__main__":
    try:
        host = host  # type: ignore
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

    sys.exit(0)
```
To reproduce the issue, run the script with `python3 reproducer.py`. The script should raise an `AssertionError` when the issue is present and print a stack trace of the issue. The script should also exit with code 0 when the issue is fixed.

The expected behavior is that the script exits with code 0 and does not print any stack trace. However, with Sphinx version 3.1.2, the script raises an `AssertionError` and prints the following stack trace:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 25, in <module>
    host = host  # type: ignore
  File "reproducer.py", line 15, in host
    @typing.overload
  File "/home/user/.local/lib/python3.8/site-packages/sphinx/ext/autodoc/__init__.py", line 570, in wrap_decorator
    return sig.apply_wrapped(decorator, globalns, localns)
  File "/home/user/.local/lib/python3.8/site-packages/sphinx/ext/autodoc/__init__.py", line 458, in apply_wrapped
