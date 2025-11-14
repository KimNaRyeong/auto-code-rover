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
    slug = models.SlugField(max_length=50)

def get_object_or_404(klass, *args, **kwargs):
    try:
        return klass.objects.get(*args, **kwargs)
    except klass.DoesNotExist:
        raise HttpResponseNotFound('Not found')

class OfferView(TemplateView):
    template_name = "offers/offer.html"

    def get_context_data(self, **kwargs):
        offer_slug = kwargs.get("offer_slug", "")
        offer = get_object_or_404(Account, slug=offer_slug)
        return {"offer": offer, "offer_slug": offer_slug}

def main():
    os.environ['DJANGO_SETTINGS_MODULE'] = 'reproducer.settings'
    setup_test_environment()
    
    from django.conf import settings
    settings.configure(
        DEBUG=True,
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:'
            }
        },
        INSTALLED_APPS=[
            'django.contrib.contenttypes',
            'django.contrib.auth',
        ],
        TEMPLATES=[
            {
                'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'APP_DIRS': True,
            },
        ]
    )
    
    from django import setup
    setup()
    
    from reproducer.urls import urlpatterns
    
    try:
        view = OfferView.as_view()
        response = view(request={'REQUEST_METHOD': 'GET'}, offer_slug='test-offer')
        assert isinstance(response, TemplateResponse)
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue is present")
    
    teardown_test_environment()

if __name__ == "__main__":
    main()
```
This script sets up a minimal Django project with a SQLite database and defines the `OfferView` class that reproduces the issue. It then tries to render the view with an `offer_slug` parameter, which should raise an `AssertionError` if the issue is present.

To run this script, create a new directory for your project, add a `reproducer` directory inside it, and create the following files:

* `reproducer/reproducer/urls.py`:
```
from django.urls import path
from .views import OfferView

urlpatterns = [
    path('/offers/<slug:offer_slug>/', OfferView.as_view(), name='offer_view'),
]
```
* `reproducer/reproducer/views.py`: empty file
* `reproducer/reproducer/templates/offers/offer.html`: empty file (just create an empty file)

Then, run the script with `python3 reproducer.py`. If the issue is present, it should raise an `AssertionError` and print a stack trace.