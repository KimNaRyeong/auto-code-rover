 Here is a standalone python file `reproducer.py` to reproduce the issue:
```python
from sympy.parsing.sympy_parser import (
    parse_expr,
    standard_transformations,
