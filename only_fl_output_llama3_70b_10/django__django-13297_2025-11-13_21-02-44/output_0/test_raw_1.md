Here is the standalone Python file `reproducer.py` to reproduce the issue:
```
import os
import sys
from django.test.utils import setup_test_environment, teardown_test_environment
from django.urls import path, re_path
from django.http import HttpResponseNotFound
from django.template.response import TemplateResponse
from django.views.generic.base import TemplateView
from django.db.models import Model

class Account(Model):
    slug = 'test-slug'

def get_object_or_404(klass, *args, **kwargs):
    return Account(slug='test-slug')

def print_stacktrace(e: Exception):
    import traceback
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

try:
    from django.urls import include
except ImportError:
    from django.conf.urls.defaults import *

urlpatterns = [
    path('offers/<slug:offer_slug>/', OfferView.as_view(), name='offer_view'),
]

class OfferView(TemplateView):
    template_name = "offers/offer.html"

    def get_context_data(self, **kwargs):
        offer_slug = kwargs.get("offer_slug", "")
        offer = get_object_or_404(Account, slug=offer_slug)
        return {"offer": offer, "offer_slug": offer_slug}

def main():
    try:
        response = OfferView.as_view()(request={'REQUEST_METHOD': 'GET', 'PATH_INFO': '/offers/test-slug/'})
        assert isinstance(response, TemplateResponse)
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue is present")

if __name__ == '__main__':
    main()
```
This script sets up a Django test environment, defines a simple model and view, and then tries to render the view with a URL parameter. If the issue is present, it will raise an `AssertionError` with a stack trace of the error.