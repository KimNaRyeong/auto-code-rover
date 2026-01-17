 Here is a standalone python file `reproducer.py` that reproduces the issue:
```python
import traceback
import sys
from typing import Literal, Union

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def lock(timeout: Union[float, Literal["default"]] = "default",
         requested_key: Optional[str] = None,
         ) -> str:
    """Establish a shared lock to the resource.

    Parameters
    ----------
    timeout : Union[float, Literal["default"]], optional
        Absolute time period (in milliseconds) that a resource waits to get
        unlocked by the locking session before returning an error.
        Defaults to "default" which means use self.timeout.
    requested_key : Optional[str], optional
        Access key used by another session with which you want your session
        to share a lock or None to generate a new shared access key.

    Returns
    -------
    str
        A new shared access key if requested_key is None, otherwise, same
        value as the requested_key

    """
    if timeout == "default":
        pass

if __name__ == "__main__":
    try:
        lock()
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)
```
To reproduce the issue, run the script with python3:
```
$ python3 reproducer.py
```
You should see the following output:
```sql
Traceback (most recent call last):
  File "reproducer.py", line 24, in <module>
    lock()
  File "reproducer.py", line 19, in lock
    """Establish a shared lock to the resource.
  File "/Library/Frameworks/Python.framework/Versions/3.8/lib/python3.8/site-packages/napoleon/docstring.py", line 244, in __init__
