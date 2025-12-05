 Here is a standalone Python file `reproducer.py` that reproduces the issue:
```python
from django.forms import BaseFormSet, formset_factory
from django.utils.functional import cached_property

class MyModel:
    a_field = ''

