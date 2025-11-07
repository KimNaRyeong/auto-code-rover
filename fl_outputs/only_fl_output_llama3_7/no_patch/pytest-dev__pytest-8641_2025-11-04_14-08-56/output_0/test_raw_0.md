Here is the reproducer script:

```python
import logging
from pytest import main
from _pytest.logging import ColoredLevelFormatter, LEVELNAME_FMT_REGEX

def test_reproducer():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(funcName)-40.40s L%(lineno)-.4d %(levelname)-5.5s| %(message)s',
                        datefmt='%Y-%m-%dT%H:%M:%S')
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.info('Test message')

if __name__ == '__main__':
    try:
        main(['-vv', '-k', 'test_reproducer'])
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

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

```

This script sets up a basic logging configuration with the given format string, logs an info message, and then runs pytest to reproduce the issue. If the issue is present, it prints the stack trace using the provided function and exits with code 1.