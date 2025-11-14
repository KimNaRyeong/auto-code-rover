Here is the reproducer script:

```python
import django
from django.forms.formsets import ManagementForm
from django.test.utils import override_settings

def main():
    try:
        formset = ManagementForm(prefix='articles')
        formset.is_valid()
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Expected exception not raised")

if __name__ == "__main__":
    main()
```

You can run this script by executing `python3 reproducer.py`. If the issue is present, it will raise an `AssertionError` and print a stack trace.