Here is the reproducer script:

```python
import os
import sys
from django.db import models
from django.db.models.fields import DecimalField
from decimal import Decimal, getcontext

def main():
    try:
        # Create a new Django project
        os.system("django-admin startproject nanbug")
        
        # Move into the project directory
        os.chdir("nanbug")
        
        # Install required packages
        os.system("pip install -r requirements.txt")
        
        # Create a model with a DecimalField
        getcontext().prec = 5
        class MyModel(models.Model):
            value = models.DecimalField(max_digits=10, decimal_places=5)
        
        # Create a model instance with value=float('nan')
        obj = MyModel(value=Decimal(float('nan')))
        obj.save()
        
        # Try to retrieve the object from the database
        retrieved_obj = MyModel.objects.get(id=obj.id)
        
    except AssertionError:
        print("Issue reproduced successfully")
        print_stacktrace(sys.exc_info()[1])
    except Exception as e:
        print(f"Issue not reproduced: {e}")
        print_stacktrace(e)

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

if __name__ == "__main__":
    main()
```

This script creates a new Django project, installs the required packages, defines a model with a DecimalField, creates a model instance with value=float('nan'), and tries to retrieve the object from the database. If the issue is reproduced, it prints "Issue reproduced successfully" and the stack trace of the exception.