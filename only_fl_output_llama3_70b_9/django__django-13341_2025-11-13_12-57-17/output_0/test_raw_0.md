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
    response = view(None, 'test-slug')
    assert isinstance(response.context_data['offer_slug'], str)
except Exception as e:
    print_stacktrace(e)
    raise AssertionError("Issue is present")
else:
    print("Issue is fixed")
```
This script sets up a minimal Django project with a `TemplateView` that reproduces the issue. It then calls the view with an example slug and checks if the `offer_slug` in the context data is a string. If it's not, it raises an `AssertionError` with a stack trace of the issue.

To run this script, create a new Django project with `django-admin startproject reproducer`, then create a new app with `python manage.py startapp reproducer_app`. Move the `reproducer.py` file to the root directory of the project and execute it with `python3 reproducer.py`.

Note that you need to have Django 3.1 installed to reproduce the issue.