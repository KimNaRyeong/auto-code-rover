```python
# reproducer.py
from django.conf import settings
from django.db import models
from django.core.management import execute_from_command_line
import os
import sys

# Minimal Django settings
settings.configure(
    DEBUG=True,
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'mydatabase',
        }
    },
    INSTALLED_APPS=(
        '__main__',
    ),
    USE_TZ=True,
)

# Define models inline to keep the example self-contained
class ModelA(models.Model):
    pass

class ModelB(models.Model):
    pass

class ModelC(models.Model):
    model_a = models.ForeignKey(ModelA, on_delete=models.CASCADE)
    model_b = models.ForeignKey(ModelB, on_delete=models.CASCADE)


def print_stacktrace(e: Exception):
    import traceback, sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)


def main():
    # Setup Django environment
    os.environ['DJANGO_SETTINGS_MODULE'] = '__main__'
    execute_from_command_line(['manage.py', 'migrate'])

    # Reproduce the issue
    try:
        query_1 = ModelC.objects.select_related('model_a')
        print('QUERY 1:', str(query_1.query))
        query_2 = query_1.select_related('model_b')
        print('QUERY 2:', str(query_2.query))
        print('QUERY 1:', str(query_1.query))
        
        assert str(query_1.query) != str(query_2.query), "The two queries are the same but should be different"
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)

    # Exit with code 0 when the issue is fixed
    print("Success: The issue is fixed.")
    sys.exit(0)

if __name__ == '__main__':
    main()
```