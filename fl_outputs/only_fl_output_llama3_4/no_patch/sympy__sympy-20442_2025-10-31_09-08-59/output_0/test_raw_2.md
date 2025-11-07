Here is the reproducer script:

```python
import sympy as sp

def main():
    J = sp.joule*sp.second
    result = sp.convert_to(J*sp.second, sp.joule)
    assert result == J*sp.second, "Expected unchanged original expression"
    if result != J*sp.second:
        raise AssertionError("convert_to seems to combine orthogonal units")
    else:
        print("Test passed")

if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print_stacktrace(e)
```

This script will raise an `AssertionError` when the issue is present and print a stack trace of the issue.