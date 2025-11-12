Here is the reproducer script:

```python
import os
import sys
from django.db import models
from django.apps import apps
from django.core.exceptions import AssertionError
from django.conf import settings

def print_stacktrace(e: Exception):
    import traceback
    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def main():
    try:
        settings.configure()
        apps.populate([models.ModuleLoader('app', os.path.join(os.getcwd(), 'app'))])
        parent_model = models.load_app('app').get_model('Parent')
        proxy_parent_model = models.load_app('app').get_model('ProxyParent')
        child_model = models.load_app('app').get_model('Child')
        many_to_many_model = models.load_app('app').get_model('ManyToManyModel')

        if not hasattr(many_to_many_model, 'through_fields') or not isinstance(many_to_many_model.through_fields, list):
            raise AssertionError("Expected ManyToManyRel to have a list of through fields")

    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == "__main__":
    main()
```

This script will attempt to load the models and check if `ManyToManyModel.through_fields` is a list. If it's not, it will raise an `AssertionError`, which should be caught by the `try-except` block and print the stack trace before exiting with code 1.

Please note that you need to have Django installed in your Python environment for this script to work.