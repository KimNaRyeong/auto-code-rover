Here is the reproducer script:

```python
import functools
from functools import wraps, partial

def logger(func):
	@wraps(func)
	def inner(*args, **kwargs):
		try:
			result = func(*args, **kwargs)
		except Exception as e:
			result = str(e)
		finally:
			print(f"{func.__name__} called with args: {args} and kwargs: {kwargs} resulting: {result}")
	return inner

class Test:
	@logger
	def hello_world(self):
		return "hello"

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

try:
	@logger
	def test_method():
		return "test"
	test_method()
except Exception as e:
	print_stacktrace(e)
	assert False, "Expected functools.partial object to have __name__ attribute"

exit(0 if "functools.partial" in str(e) else 1)
```

This script should raise an `AssertionError` when the issue is present and print a stack trace of the issue.