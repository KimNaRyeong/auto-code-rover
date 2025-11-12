Here is the reproducer script:

```python
import subprocess
import sys
from io import StringIO

def main():
    try:
        command = ["./manage.py", "dbshell", "--", "-c", "select * from some_table;"]
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()
        if b"psql: warning: extra command-line argument \"select * from some_table;\" ignored" in error:
            raise AssertionError("Issue reproduced")
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

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

if __name__ == "__main__":
    main()
```

To run the reproducer, execute `python3 reproducer.py` in your terminal.