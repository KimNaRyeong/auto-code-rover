# reproducer.py
import django
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.forms import ModelForm

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

# Setup minimal Django environment
settings.configure(
    DATABASES={"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}},
    INSTALLED_APPS=["__main__"],
    TIME_ZONE="UTC",
    USE_TZ=True,
)

django.setup()

# Define a minimal model and form
class DummyModel(models.Model):
    json_field = models.JSONField(null=True, blank=True)

class DummyModelForm(ModelForm):
    class Meta:
        model = DummyModel
        fields = ['json_field']

try:
    # Attempt to create a form with an unbound field.
    form = DummyModelForm({})
    
    # This should not raise an error but will if the issue is present.
    form_content = form.as_p()
except ValidationError as e:
    print_stacktrace(e)
    exit(1)
except TypeError as e:
    print_stacktrace(e)
    # Exit with assertion error indicating the reproduction of the issue.
    raise AssertionError("Issue reproduced: JSONField.bound_data raises TypeError when data is None")
except Exception as e:
    print_stacktrace(e)
    exit(1)

print("No issues encountered.")
# Indicating the issue is fixed if none of the above exceptions are raised.
exit(0)
