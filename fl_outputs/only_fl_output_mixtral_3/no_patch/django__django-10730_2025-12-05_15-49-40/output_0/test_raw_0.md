 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
class WrapperException(Exception):
    def __init__(self, exc_value=None):
        self.exc_value = exc_value
