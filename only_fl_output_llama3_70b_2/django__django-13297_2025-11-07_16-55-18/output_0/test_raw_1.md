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

os.environ['DJANGO_SETTINGS_MODULE'] = 'reproducer.settings'

import reproducer.settings

setup_test_environment()

from django.test.client import RequestFactory
factory = RequestFactory()

class OfferView(TemplateView):
    template_name = "offers/offer.html"
    def get_context_data(self, **kwargs):
        offer_slug = kwargs.get("offer_slug", "")
        offer = get_object_or_404(Account, slug=offer_slug)
        return {"offer": offer, "offer_slug": offer_slug}

urlpatterns = [
    path('offers/<slug:offer_slug>/', OfferView.as_view(), name='offer_view'),
]

try:
    request = factory.get('/offers/test-slug/')
    response = OfferView.as_view()(request, offer_slug='test-slug')
    assert isinstance(response.context_data['offer_slug'], str)
except Exception as e:
    print_stacktrace(e)
    sys.exit(1)

sys.exit(0)
```
This script sets up a Django test environment, defines a simple model and view, and then tries to render the view with a URL parameter. If the issue is present, it will raise an `AssertionError` when trying to access the `offer_slug` context variable, which should be a string but is actually a `SimpleLazyObject`. The script will print the stack trace of the error using the provided `print_stacktrace` function and exit with code 1. If the issue is fixed, the script will exit with code 0.