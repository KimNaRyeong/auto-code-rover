Here is the reproducer script:

```python
import os
from django.db import models
from django.apps import apps
from django.core.exceptions import ImproperlyConfigured

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
    os.environ['DJANGO_SETTINGS_MODULE'] = 'django_related_name_bug.settings'
    
    class Model1(models.Model):
        model2 = models.ManyToManyField('Model2', related_name='+')

    class Model2(models.Model):
        pass

    try:
        models.check_models_order()
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Expected error not raised")

    if os.path.exists('django_related_name_bug'):
        os.rmdir('django_related_name_bug')
    else:
        os.makedirs('django_related_name_bug')

if __name__ == "__main__":
    main()
```

This script creates a directory named 'django_related_name_bug' in the current working directory. It then defines two models with ManyToManyFields and related_name='+', and tries to run `models.check_models_order()`. If an error is raised, it prints the stack trace and raises an AssertionError.