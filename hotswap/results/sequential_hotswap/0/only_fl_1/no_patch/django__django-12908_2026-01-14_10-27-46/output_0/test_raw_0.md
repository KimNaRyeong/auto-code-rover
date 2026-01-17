Below is a standalone Python script `reproducer.py` tailored to reproduce the described issue. This script presumes a Django environment since it deals with Django ORM specifics like Model definitions, querying with `.annotate()`, `.filter()`, and `.union()`, followed by `.distinct()`. For the purpose of this example, I'm simplifying the context around user and sample creation, assuming a minimal but sufficient Django setup is present.

Before executing this script, ensure your Django environment is set up with a `Sample` model, and the necessary settings are configured (e.g., database settings in `settings.py`).

```python
import os
import django
from django.db import models
from django.db.models import Value, IntegerField

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')
django.setup()

# Definition for `Sample` model (assuming it exists)
# If it does not exist, you will need to define it accordingly in your models.py file
# and execute migrations before running this script.
class Sample(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    class Meta:
        app_label = 'your_app_label_here'

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
        # Assuming `your_user_variable` is an instance of the User model.
        # Replace it with an actual instance according to your scenario.
        user = your_user_variable
        
        # Sample data creation
        Sample.objects.create(user=user, name="Sam1")
        Sample.objects.create(user=user, name="Sam2 acid")
        Sample.objects.create(user=user, name="Sam3")
        Sample.objects.create(user=user, name="Sam4 acid")
        Sample.objects.create(user=user, name="Dub")
        Sample.objects.create(user=user, name="Dub")
        Sample.objects.create(user=user, name="Dub")

        # Test case from the description
        qs = Sample.objects.filter(user=user)
        qs1 = qs.filter(name='Dub').annotate(rank=Value(0, IntegerField()))
        qs2 = qs.filter(name='Sam1').annotate(rank=Value(1, IntegerField()))
        qs = qs1.union(qs2)
        qs = qs.order_by('name').distinct('name')  # This is expected to not work properly
        assert qs.count() == 2, "Distinct operation on union'ed queryset did not work as expected."

    except Exception as e:
        print_stacktrace(e)
        exit(1)  # Exits with error code when an issue is encountered

if __name__ == '__main__':
    main()
    print("Script executed successfully, no issues detected.")
```

**Important Note:**
- Replace `'your_project.settings'` with your actual Django project settings module path.
- Replace `your_app_label_here` in the `Sample` model definition's Meta class with the actual app label where your `Sample` model is defined.
- Ensure you have a valid user instance in place of `your_user_variable` or adjust the script to create or fetch a suitable user before creating `Sample` instances.
- You must have Django and your project environment properly set up, including applied migrations for the `Sample` model, for this script to run successfully.