import os
import django
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.urls import get_resolver, resolve, Resolver404
from django.utils.translation import get_language_from_path
import traceback
import sys

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def test_issue():
    # Set up Django project
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test_project.settings')
    settings.configure(
        DEBUG=True,
        LANGUAGE_CODE='es',
        LOCALE_PATHS=['/path/to/locale'],
        ROOT_URLCONF='test_project.urls',
        SITE_ID=1,
        USE_I18N=True,
        USE_L10N=True,
        USE_THOUSAND_SEPARATOR=True,
    )
    django.setup()

    # Create resolver
    resolver = get_resolver()

    # Test with prefix_default_language=True
    settings.MIDDLEWARE = [
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.locale.LocaleMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        'django.middleware.security.SecurityMiddleware',
    ]
    assert get_language_from_path('/es/') == 'es'
    assert resolver.resolve('/es/').func.__name__ == 'test_view'

    # Test with prefix_default_language=False
    settings.MIDDLEWARE = [
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        'django.middleware.security.SecurityMiddleware',
    ]
    settings.LANGUAGE_CODE = 'es'
    try:
        resolver.resolve('/')
    except Resolver404 as e:
        print_stacktrace(e)
        raise AssertionError('HTTP 404 raised as expected')

if __name__ == '__main__':
    try:
        test_issue()
    except ImproperlyConfigured as e:
        print_stacktrace(e)
        raise AssertionError('ImproperlyConfigured raised as expected')
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError('Unexpected exception raised')
