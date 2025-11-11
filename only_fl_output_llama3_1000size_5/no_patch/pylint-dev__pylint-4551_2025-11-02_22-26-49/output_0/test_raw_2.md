Here is the reproducer script:

```python
import pyreverse
from your_module import C  # Replace 'your_module' with the actual module name where you defined class C

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

def main():
    try:
        # Call the method that should raise an error when type hints are not used
        pyreverse.generate(C())
    except Exception as e:
        print_stacktrace(e)
        assert False, "Expected pyreverse to read type hints"

if __name__ == "__main__":
    main()
```

Please replace `'your_module'` with the actual module name where you defined class `C`.