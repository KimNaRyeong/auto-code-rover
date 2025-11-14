Here is the standalone Python file `reproducer.py` to reproduce the issue:
```
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'reproducer.settings'

import django
django.setup()

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.views.generic import TemplateView

class OfferView(TemplateView):
    template_name = "offer.html"

    def get_context_data(self, **kwargs):
        offer_slug = kwargs.get("offer_slug", "")
        offer = get_object_or_404(Account, slug=offer_slug)
        return {"offer": offer, "offer_slug": offer_slug}

class Account:
    def __init__(self, slug):
        self.slug = slug

def view(request, offer_slug):
    return OfferView.as_view()(request, offer_slug=offer_slug)

try:
    response = view(None, 'test-offer')
    assert isinstance(response.context_data['offer_slug'], str)
except Exception as e:
    print_stacktrace(e)
    raise AssertionError("Issue is present")
```
This script sets up a minimal Django project with a `TemplateView` that reproduces the issue. It defines an `OfferView` class that inherits from `TemplateView`, and a `view` function that calls the view with a sample `offer_slug` argument.

The script then tries to render the view and checks if the `offer_slug` value in the context data is a string. If it's not, it raises an `AssertionError` with a stack trace of the issue using the provided `print_stacktrace` function.

To run this script, create a new Django project with `django-admin startproject reproducer`, then add the `reproducer.py` file to the root directory of the project. Run the script with `python3 reproducer.py`. If the issue is present, it should raise an `AssertionError` with a stack trace.