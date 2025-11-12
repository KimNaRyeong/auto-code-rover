Here is the reproducer script:

```python
import django
from django.forms.formsets import BaseFormSet, ManagementForm
from django.utils.datastructures import MergeDict

def main():
    try:
        formset = SomeFormSet(MergeDict({'INITIAL_FORMS': '1', 'MAX_NUM_FORMS': '10', 'TOTAL_FORMS': '2'}), prefix='articles')
        formset.is_valid()
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Expected exception not raised")

class SomeFormSet(BaseFormSet):
    def __init__(self, data=None, files=None, prefix='', queryset=None):
        super(SomeFormSet, self).__init__(data=data, files=files, prefix=prefix, queryset=queryset)

if __name__ == "__main__":
    main()
```

This script creates a `SomeFormSet` with incorrect prefix and then tries to validate it. If the expected exception is not raised, the script will fail with an `AssertionError`.