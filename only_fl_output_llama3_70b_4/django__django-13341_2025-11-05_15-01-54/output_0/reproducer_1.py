import os
import sys
from django.conf import settings
from django.test.utils import setup_test_environment, teardown_test_environment
from django.urls import path
from django.http import HttpResponseNotFound
from django.template.response import TemplateResponse
from django.views.generic.base import TemplateView

settings.configure(DEBUG=True, INSTALLED_APPS=['reproducer'])

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

setup_test_environment()

from django.test.client import RequestFactory
rf = RequestFactory()

class OfferView(TemplateView):
    template_name = "offers/offer.html"
    def get_context_data(self, **kwargs):
        offer_slug = kwargs.get("offer_slug", "")
        return {"offer_slug": offer_slug}

urlpatterns = [
    path("/offers/<slug:offer_slug>/", OfferView.as_view(), name="offer_view"),
]

try:
    request = rf.get('/offers/test-slug/')
    response = OfferView.as_view()(request, offer_slug='test-slug')
    assert isinstance(response, TemplateResponse)
    # Simulate the issue by trying to use the SimpleLazyObject
    offer_slug_lazy = kwargs.get("offer_slug", "")
    get_object_or_404(Account, slug=offer_slug_lazy)  # This should raise an error
except Exception as e:
    print_stacktrace(e)
    raise AssertionError("Issue is present")

teardown_test_environment()
sys.exit(0 if 'SimpleLazyObject' in str(sys.last_value) else 1)
