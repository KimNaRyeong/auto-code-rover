Here is the reproducer script:

```python
import django
from django.views.debug import SafeExceptionReporterFilter

def reproduce_issue():
    try:
        settings = {1: {'login': 'cooper', 'password': 'secret'}}
        SafeExceptionReporterFilter().cleanse_setting(settings)
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue reproduced")

if __name__ == "__main__":
    reproduce_issue()
```

This script imports the `SafeExceptionReporterFilter` from Django's debug module, defines a function `reproduce_issue()` that attempts to clean a settings dictionary with non-string keys using the filter, and then prints the stack trace of any exception raised. If an assertion error is raised, it means the issue was reproduced successfully.

To run this script, save it in a file named `reproducer.py` at the root directory of your project, and execute it with Python 3: `python3 reproducer.py`.