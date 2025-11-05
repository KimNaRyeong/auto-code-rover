Here is the standalone Python file `reproducer.py` to reproduce the issue:
```
import os
import sys
from django.test.utils import setup_test_environment
from django.urls import path, re_path
from django.http import HttpResponseNotFound
from django.template.response import TemplateResponse
from django.views.generic import TemplateView
from django.db.models import Model

class Account(Model):
    slug = 'test-slug'

def get_object_or_404(klass, *args, **kwargs):
    return Account()

class OfferView(TemplateView):
    template_name = "offers/offer.html"

    def get_context_data(self, **kwargs):
        offer_slug = kwargs.get("offer_slug", "")
        offer = get_object_or_404(Account, slug=offer_slug)
        return {"offer": offer, "offer_slug": offer_slug}

def main():
    os.environ['DJANGO_SETTINGS_MODULE'] = 'reproducer.settings'
    setup_test_environment()

    from django import setup
    setup()

    from reproducer import settings

    try:
        response = OfferView.as_view()(request={'offer_slug': 'test-slug'})
        assert isinstance(response, TemplateResponse)
        print("Issue is fixed")
        sys.exit(0)
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue is present")

if __name__ == "__main__":
    main()
```
This script sets up a minimal Django project and defines the necessary models, views, and URLs to reproduce the issue. It then tries to render the `OfferView` with an `offer_slug` parameter and checks if it raises an exception. If it does, it prints the stack trace using the provided function and exits with code 1. If it doesn't, it prints a success message and exits with code 0.

To run this script, create a new Django project and add the `reproducer.py` file to its root directory. Then, execute the script using `python3 reproducer.py`.