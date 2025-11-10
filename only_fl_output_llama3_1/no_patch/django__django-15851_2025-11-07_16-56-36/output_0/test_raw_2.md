Here is the reproducer script `reproducer.py`:

```python
import subprocess
import sys
from io import StringIO
import os

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

def reproduce_issue():
    try:
        command = ["psql", "--username=myuser", "mydatabase", "-c", "select * from some_table;"]
        output = subprocess.check_output(command, stderr=subprocess.STDOUT)
        if not output.decode().strip():
            raise AssertionError("Expected error message")
    except subprocess.CalledProcessError as e:
        print_stacktrace(e)

if __name__ == "__main__":
    reproduce_issue()
    sys.exit(0)
```

This script attempts to execute the command `psql --username=myuser mydatabase -c "select * from some_table;"` and checks if the output is empty. If not, it raises an `AssertionError`. The `print_stacktrace` function is used to print the stack trace of any exceptions that occur during execution.

To run this script, save it as `reproducer.py`, navigate to its directory in your terminal, and execute it with `python3 reproducer.py`.

Please note that you need to replace `"myuser"` and `"mydatabase"` with your actual PostgreSQL username and database name.