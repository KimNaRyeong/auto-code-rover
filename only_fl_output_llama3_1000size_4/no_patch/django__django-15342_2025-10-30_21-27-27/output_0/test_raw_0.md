Here is the reproducer script:

```python
import os
import sys
from django.db import models
from django.db.migrations.state import ModelState

def main():
    class Model(models.Model):
        _order = models.IntegerField()

    model_state = ModelState()
    try:
        model_state.get_field('_order')
    except KeyError as e:
        print_stacktrace(e)
        raise AssertionError("Expected KeyError")

if __name__ == "__main__":
    main()
```

To run the script, save it to a file named `reproducer.py` and execute it with Python:

```bash
python3 reproducer.py
```

This should output the stack trace of the issue.