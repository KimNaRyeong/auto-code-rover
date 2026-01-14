 Here is a standalone python file `reproducer.py` to reproduce the issue:
```python
import sys
import traceback
from typing import TypeVar, Type

import sphinx
from sphinx.ext.autodoc import mock

T = TypeVar("T")


class GenericClass(genericClass):
    def __init__(self, value: T):
        self.value = value
