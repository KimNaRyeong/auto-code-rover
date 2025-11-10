Here is the `reproducer.py` file that reproduces the issue:
```
import os
import sys
from django.test.utils import setup_test_environment, teardown_test_environment
from django.urls import path, re_path
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.views.generic import TemplateView
from django.db.models import Model

class Account(Model):
    slug = 'test'

def get_object_or_404(klass, *args, **kwargs):
    return Account()

class OfferView(TemplateView):
    template_name = "offer.html"
    def get_context_data(self, **kwargs):
        offer_slug = kwargs.get("offer_slug", "")
        offer = get_object_or_404(Account, slug=offer_slug)
        return {"offer": offer, "offer_slug": offer_slug}

def main():
    os.environ['DJANGO_SETTINGS_MODULE'] = 'reproducer.settings'
    setup_test_environment()
    
    try:
        from django import setup
        setup()
        
        from reproducer import settings
        
        urlpatterns = [
            path('offers/<slug:offer_slug>/', OfferView.as_view(), name='offer_view'),
        ]
        
        from django.test.client import RequestFactory
        factory = RequestFactory()
        request = factory.get('/offers/test/')
        response = OfferView.as_view()(request, offer_slug='test')
        
        if isinstance(response.context_data['offer_slug'], str):
            print("Issue is fixed")
            sys.exit(0)
        else:
            raise AssertionError("Issue is present")
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == "__main__":
    main()
```
This script sets up a minimal Django project, defines an `Account` model and an `OfferView` that reproduces the issue. It then creates a request to the view and checks if the `offer_slug` in the context data is a string or a `SimpleLazyObject`. If it's a string, it means the issue is fixed and the script exits with code 0. Otherwise, it raises an `AssertionError` with a stack trace of the issue.

Note that you'll need to create a `reproducer/settings.py` file with the following content:
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.auth',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
    },
]
```
This sets up a minimal Django project with an in-memory SQLite database and the necessary settings for the script to run.