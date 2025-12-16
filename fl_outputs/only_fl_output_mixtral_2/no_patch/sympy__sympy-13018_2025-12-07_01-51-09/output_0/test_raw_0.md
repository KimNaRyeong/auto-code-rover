 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
import sympy
from reproducer import print_stacktrace

def test_pow_subs():
    sympy.__version__  #