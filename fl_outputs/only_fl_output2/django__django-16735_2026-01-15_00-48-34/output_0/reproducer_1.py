# reproducer.py

import os
import sys

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

def setup_django_environment():
    # Setting up a minimal django environment
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reproducer.settings')
    from django.conf import settings

    settings.configure(
        DEBUG=True,
        SECRET_KEY='foobar',
        ROOT_URLCONF=__name__,
        MIDDLEWARE=[
            'django.middleware.common.CommonMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.middleware.security.SecurityMiddleware',
        ],
        INSTALLED_APPS=[
            'django.contrib.admin',
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
        ],
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            },
        },
        USE_I18N=True,
        USE_L10N=True,
        USE_TZ=True,
        LANGUAGE_CODE='en',
        LANGUAGES=(
            ('en', 'English'),
            ('de', 'German'),
        ),
    )

    import django
    django.setup()

    from django.urls import path, include
    from django.contrib import admin
    from django.conf.urls.i18n import i18n_patterns

    global urlpatterns
    urlpatterns = i18n_patterns(
        path('admin/', admin.site.urls),
        prefix_default_language=False,
    )

def run_server_test():
    from django.test import Client
    client = Client()

    # By default, Django will add a trailing slash, hence '/admin/' is used
    response = client.get('/admin/', follow=False)
    is_redirected = response.status_code in [301, 302]
    
    if is_redirected:
        final_url = response.url
        assert final_url != '/en/admin/', 'Unexpectedly redirected to prefixed default language URL /en/admin/'
    else:
        assert response.status_code == 200, 'Expected 200 response when accessing /admin/ directly'

if __name__ == "__main__":
    try:
        setup_django_environment()
        run_server_test()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
    except Exception as e:
        print_stacktrace(e)
        exit(1)
    else:
        print("No issue detected. /admin/ was accessed without a language prefix as expected.")
        exit(0)
