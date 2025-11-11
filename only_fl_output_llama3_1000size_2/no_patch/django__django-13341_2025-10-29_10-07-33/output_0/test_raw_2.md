Here is the reproducer script:

```python
from django.urls import path, include
from django.views.generic import TemplateView
from django.db.models import get_object_or_none
import sys
import traceback

def print_stacktrace(e: Exception):
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
        class OfferView(TemplateView):
            template_name = "offers/offer.html"

            def get_context_data(self, **kwargs):
                offer_slug = kwargs.get("offer_slug", "")
                offer = get_object_or_none(Account, slug=offer_slug)
                return {"offer": offer, "offer_slug": offer_slug}

        path("/offers/<slug:offer_slug>/", OfferView.as_view(), name="offer_view")

    except Exception as e:
        print_stacktrace(e)
        assert False, "Expected error"

if __name__ == "__main__":
    main()
```

This script will raise an `AssertionError` when the issue is present and print a stack trace of the issue. It will also exit with code 0 when the issue is fixed.

To run this script, save it in a file named `reproducer.py`, then execute it using `python3 reproducer.py`.