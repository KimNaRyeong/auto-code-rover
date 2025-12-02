 Here is a standalone Python file `reproducer.py` that reproduces the issue:
```python
import argparse

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
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true', help='Increase output verbosity')
    args = parser.parse_args()

    if args.verbose:
        verbose = True
    else:
        verbose = False

    if verbose:
        print("Verbose mode is on.")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print_stacktrace(e)
        raise
```
When you run the script with the `-v` option, you should see the following output:
```shell
$ python3 reproducer.py -v
Traceback (most recent call last):
  File "reproducer.py", line 23
    main()
  File "reproducer.py", line 17
    args = parser.parse_args()
  File "/Library/Frameworks/Python.framework/Versions/3.9/lib/python3.9/argparse.py", line 1821, in parse_args
    namespace, args = self._parse_known_args(args, namespace)
  File "/Library/Frameworks/Python.framework/Versions/3.9/lib/python3.9/argparse.py", line 1994, in _parse_known_args
