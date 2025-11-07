Here is the reproducer script:

```python
import argparse
import sys

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', help='Verbose mode')
    args, _ = parser.parse_known_args()

    if args.verbose:
        print("Verbose mode enabled")
    else:
        print("Verbose mode disabled")

if __name__ == "__main__":
    try:
        main()
    except SystemExit as e:
        if e.code != 0:
            raise
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
    try:
        main()
    except SystemExit as e:
        if e.code != 0:
            raise
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)
```

You can run this script with `python3 reproducer.py` and it should reproduce the issue.