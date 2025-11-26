import os
import django
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.views.generic import TemplateView

# Create a minimal Django project structure
os.makedirs('project', exist_ok=True)
with open('project/settings.py', 'w') as f:
    f.write("INSTALLED_APPS = ['django.contrib.contenttypes']\nDATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3'}}")

os.environ['DJANGO_SETTINGS_MODULE'] = 'project.settings'

# Initialize Django
django.setup()

class Account:
    def __init__(self, slug):
        self.slug = slug

def get_object_or_404(klass, *args, **kwargs):
    return Account(slug='test-offer')

class OfferView(TemplateView):
    template_name = "offer.html"

    def get_context_data(self, **kwargs):
        offer_slug = kwargs.get("offer_slug", "")
        offer = get_object_or_404(Account, slug=offer_slug)
        return {"offer": offer, "offer_slug": offer_slug}

def view(request, offer_slug):
    return OfferView.as_view()(request, offer_slug=offer_slug)

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

try:
    response = view(None, 'test-offer')
    assert isinstance(response.context_data['offer_slug'], str)
except Exception as e:
    print_stacktrace(e)
    raise AssertionError("Issue is present")
else:
    print("Issue is fixed")
