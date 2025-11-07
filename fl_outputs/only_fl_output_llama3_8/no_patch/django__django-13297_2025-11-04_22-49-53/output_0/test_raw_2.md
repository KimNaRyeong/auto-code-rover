Here is the reproducer script:

```python
import django
from django.urls import path, URLResolver
from django.db.models import Q
from django.core.exceptions import ImproperlyConfigured
from django.template.response import TemplateResponse
from django.views.generic import TemplateView

def get_object_or_404(model, slug):
    if not isinstance(slug, str):
        raise TypeError("slug must be a string")
    return model.objects.get(Q(slug=slug))

class OfferView(TemplateView):
    template_name = "offers/offer.html"

    def get_context_data(self, **kwargs):
        offer_slug = kwargs.get("offer_slug", "")
        if isinstance(offer_slug, django.utils.functional.SimpleLazyObject):
            raise AssertionError("Issue present")
        offer = get_object_or_404(Account, slug=offer_slug)
        return {"offer": offer, "offer_slug": offer_slug}

def main():
    try:
        view = OfferView()
        response = view.get_context_data(offer_slug="test")
        TemplateResponse(response.context_data)
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue not fixed")

if __name__ == "__main__":
    django.setup()
    Account = type('Account', (), {'objects': lambda x: []})
    main()
```

This script sets up a minimal Django project, defines the `OfferView` and the `get_object_or_404` function, and then tries to get the context data from the view. If the `offer_slug` is of type `django.utils.functional.SimpleLazyObject`, it raises an `AssertionError`.