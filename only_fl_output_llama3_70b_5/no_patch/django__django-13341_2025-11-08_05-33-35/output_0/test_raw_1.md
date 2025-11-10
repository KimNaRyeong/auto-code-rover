Here is the standalone Python file `reproducer.py` to reproduce the issue:
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
    slug = models.SlugField(max_length=50)

def get_object_or_404(klass, *args, **kwargs):
    try:
        return klass.objects.get(*args, **kwargs)
    except klass.DoesNotExist:
        raise Http404('Not found')

class OfferView(TemplateView):
    template_name = "offer.html"

    def get_context_data(self, **kwargs):
        offer_slug = kwargs.get("offer_slug", "")
        offer = get_object_or_404(Account, slug=offer_slug)
        return {"offer": offer, "offer_slug": offer_slug}

def main():
    os.environ['DJANGO_SETTINGS_MODULE'] = 'reproducer.settings'
    setup_test_environment()
    
    from django.conf import settings
    settings.configure(
        INSTALLED_APPS=['django.contrib.contenttypes', 'django.contrib.auth'],
        DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': ':memory:'}},
        TEMPLATES=[{'BACKEND': 'django.template.backends.django.DjangoTemplates', 'APP_DIRS': True}],
    )
    
    from django import setup
    setup()
    
    from reproducer.urls import urlpatterns
    
    try:
        response = OfferView.as_view()(request={'offer_slug': 'test'})
        assert isinstance(response, TemplateResponse)
        assert response.context_data['offer_slug'] == 'test'
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue is present")
    
    teardown_test_environment()

if __name__ == "__main__":
    main()
```

And here is the `urls.py` file:
```
from django.urls import path
from .views import OfferView

urlpatterns = [
    path('offers/<slug:offer_slug>/', OfferView.as_view(), name='offer_view'),
]
```

And here is the `settings.py` file:
```
INSTALLED_APPS = ['django.contrib.contenttypes', 'django.contrib.auth']
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': ':memory:'}}
TEMPLATES = [{'BACKEND': 'django.template.backends.django.DjangoTemplates', 'APP_DIRS': True}]
```

You can run the script by executing `python3 reproducer.py` in the root directory of the project. If the issue is present, it will raise an `AssertionError` and print a stack trace of the issue. If the issue is fixed, it will exit with code 0.

Note: You need to create a `reproducer` directory in the root directory of the project and add the above files (`reproducer.py`, `urls.py`, and `settings.py`) inside it. Also, make sure you have Django installed in your Python environment.