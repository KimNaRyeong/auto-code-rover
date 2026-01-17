 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
from sympy.parsing.sympy_parser import (
    parse_expr,
    standard_transformations,
