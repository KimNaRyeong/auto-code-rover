import os
import sys
from django.conf import settings
from django.test.utils import setup_test_environment
from django.urls import path, include
from django.utils.translation import get_language_from_path

settings.configure(
    LANGUAGE_CODE='fr',  # Set default language to French
    LANGUAGES=[('en', 'English'), ('fr', 'French')],
    USE_I18N=True,
    ROOT_URLCONF=__name__,
)

def home_view(request):
    return HttpResponse("Home page")

urlpatterns = [
    path('', home_view, name='home'),
]

setup_test_environment()

from django.test.client import RequestFactory

rf = RequestFactory()

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
    request = rf.get('/')
    assert request.resolver_match.func.__name__ == 'home_view'
except Exception as e:
    print_stacktrace(e)
    raise AssertionError("Expected 200 OK, but got an error")

print("Issue not present, exiting with code 0")
sys.exit(0)
