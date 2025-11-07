# reproducer.py
import os
import django
from django.conf import settings
from django.core.management import execute_from_command_line
from django.urls import path, include
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from django.apps import apps
from django.db import models


def setup_django_environment():
    settings.configure(
        DEBUG=True,
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            },
        },
        ROOT_URLCONF=__name__,
        INSTALLED_APPS=('__main__',),
        TEMPLATES=[{
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [],
        }],
    )
    django.setup()


setup_django_environment()


class Account(models.Model):
    slug = models.SlugField(unique=True)


class OfferView(TemplateView):
    template_name = "offers/offer.html"

    def get_context_data(self, **kwargs):
        offer_slug = str(kwargs.get("offer_slug", ""))
        offer = get_object_or_404(Account, slug=offer_slug)
        return {"offer": offer, "offer_slug": offer_slug}


def offer_view(request, offer_slug):
    return HttpResponse("This is a dummy response for offer slug: " + offer_slug)


urlpatterns = [
    path('offers/<slug:offer_slug>/', OfferView.as_view(), name='offer_view'),
]


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


def main():
    execute_from_command_line(['manage.py', 'migrate'])
    try:
        # Setup test environment
        os.environ['DJANGO_SETTINGS_MODULE'] = '__main__'
        Account.objects.create(slug='test-slug')
        # Simulate a request to OfferView with an offer_slug
        from django.test import Client
        client = Client()
        response = client.get('/offers/test-slug/')
        # Check if response context contains the correct type after resolution
        assert isinstance(response.context['offer_slug'], str), "Context 'offer_slug' is not a string"
        print("Success: The issue is fixed or not present.")
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("The issue is present.")


if __name__ == '__main__':
    # Uncomment below line if you're not using Django's `manage.py` to run this script
    main()
