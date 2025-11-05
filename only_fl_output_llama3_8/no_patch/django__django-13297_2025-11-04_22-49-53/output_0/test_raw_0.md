Here is the reproducer script:

```python
import django
from django.urls import path, URLResolver
from django.db.models import Q
from django.core.exceptions import ImproperlyConfigured

def get_object_or_404(model, slug):
    if not isinstance(slug, str):
        raise TypeError("slug must be a string")
    return model.objects.get(Q(slug=slug))

class OfferView:
    template_name = "offers/offer.html"

    def get_context_data(self, **kwargs):
        offer_slug = kwargs.get("offer_slug", "")
        offer = get_object_or_404(Account, slug=offer_slug)
        return {"offer": offer, "offer_slug": offer_slug}

def main():
    try:
        URLResolver([]).resolve('/offers/<slug:offer_slug>/')
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue not fixed")

if __name__ == "__main__":
    django.setup()
    Account = type('Account', (), {'objects': lambda x: []})
    main()
```

This script sets up a minimal Django project, defines the `OfferView` and the `get_object_or_404` function, and then tries to resolve a URL that should trigger the issue. If an exception is raised, it prints the stack trace using the provided function and raises an `AssertionError`.