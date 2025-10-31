Here is a standalone Python file `reproducer.py` that reproduces the issue:

```python
import os
from django.urls import path
from django.views.generic import TemplateView
from django.db.models import SimpleLazyObject
from django.core.exceptions import ObjectDoesNotExist

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

class OfferView(TemplateView):
    template_name = "offers/offer.html"

    def get_context_data(self, **kwargs):
        offer_slug = kwargs.get("offer_slug", "")
        if isinstance(offer_slug, SimpleLazyObject):
            raise AssertionError("Expected string, got SimpleLazyObject")
        return {"offer": None, "offer_slug": offer_slug}

urlpatterns = [
    path("/offers/<slug:offer_slug>/", OfferView.as_view(), name="offer_view"),
]

if __name__ == "__main__":
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reproducer.settings')
        from django.core.wsgi import get_wsgi_application
        application = get_wsgi_application()
        request = {}
        offer_slug = SimpleLazyObject(lambda: "test")
        request["offer_slug"] = offer_slug
        OfferView().get_context_data(**request)
    except Exception as e:
        print_stacktrace(e)
        exit(1)
```

This script sets up a minimal Django project, defines the `OfferView` class with the problematic `get_context_data` method, and then attempts to call this method with a request that contains a `SimpleLazyObject` for the `offer_slug`. If the issue is present (i.e., the `SimpleLazyObject` is not converted to a string), an `AssertionError` will be raised, which will trigger the script to print the stack trace and exit with code 1.