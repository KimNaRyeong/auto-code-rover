Here is the reproducer script:

```python
import pytest
from your_module import Permutation  # Replace 'your_module' with the actual module name

def test_permutation():
    try:
        permutation = Permutation([[0,1],[0,1]])
    except Exception as e:
        print_stacktrace(e)
        assert False, "Expected Permutation constructor to succeed"

if __name__ == "__main__":
    pytest.main([__file__])
```

This script will run the test function and if the issue is present, it will print the stack trace and exit with code 1. If the issue is fixed, it will simply exit with code 0.

Please replace `'your_module'` with the actual module name where `Permutation` class is defined.