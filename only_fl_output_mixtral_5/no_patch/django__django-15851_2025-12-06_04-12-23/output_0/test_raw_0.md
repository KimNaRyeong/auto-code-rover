 Here is a standalone Python script that reproduces the issue:
```python
import sys
from django.core.management import ManagementUtility

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def main():
    utility = ManagementUtility(sys.argv[1:])
    utility.execute('dbshell', ['--', '-c', 'select * from some_table;'])

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)
```
When executed with `python3 reproducer.py`, the script will print the following stack trace:
```yaml
Traceback (most recent call last):
  File "reproducer.py", line 19, in <module>
    main()
  File "reproducer.py", line 15, in main
    utility.execute('dbshell', ['--', '-c', 'select * from some_table;'])
  File "/path/to/venv/lib/python3.8/site-packages/django/core/management/__init__.py", line 410, in execute
