Here is the reproducer script:

```python
import os
from django.urls import path
from django.views.generic import TemplateView
from django.db.models import SimpleLazyObject
from django.core.exceptions import ImproperlyConfigured

def get_object_or_404(model, slug):
    raise ImproperlyConfigured("get_object_or_404 should be called with a valid model and slug")

class OfferView(TemplateView):
    template_name = "offers/offer.html"

    def get_context_data(self, **kwargs):
        offer_slug = kwargs.get("offer_slug", "")
        offer = get_object_or_404(Account, slug=offer_slug)
        return {"offer": offer, "offer_slug": offer_slug}

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
    from django.conf import settings
    settings.configure()

    view = OfferView.as_view()
    path("/offers/<slug:offer_slug>/", view, name="offer_view")

    try:
        view(None, **{"offer_slug": SimpleLazyObject()})
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Expected exception not raised")

if __name__ == "__main__":
    main()
```

This script sets up a minimal Django environment and attempts to call the `get_context_data` method of the `OfferView`. If the issue is present, it should raise an assertion error with a stack trace.