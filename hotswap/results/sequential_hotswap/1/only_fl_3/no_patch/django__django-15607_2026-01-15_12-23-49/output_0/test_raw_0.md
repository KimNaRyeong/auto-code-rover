```python
import os
import sys
from django.conf import settings
from django.urls import path
from django.http import HttpResponse
from django.contrib.auth.views import LogoutView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.test import TestCase, Client
from django.core.wsgi import get_wsgi_application


# Configure Django settings
settings.configure(
    DEBUG=True,
    SECRET_KEY='a-very-secret-key',
    ROOT_URLCONF=__name__,
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'db.sqlite3',
        }
    },
    TEMPLATES=[
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [],
            'APP_DIRS': True,
        },
    ],
    MIDDLEWARE=[
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
    ],
    LOGOUT_REDIRECT_URL='/custom-logout-redirect-url/',
    INSTALLED_APPS=[
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
    ]
)

def logout_view(request):
    return LogoutView.as_view()(request)

# URL Configuration
urlpatterns = [
    path('logout/', logout_view, name='logout'),
]


class LogoutRedirectTestCase(TestCase):
    def setUp(self):
        self.username = 'user1'
        self.password = 'bar'
        User.objects.create_user(username=self.username, password=self.password)
        self.client = Client()
        self.logged_in = self.client.login(username=self.username, password=self.password)
        assert self.logged_in

    def test_logout_redirect(self):
        response = self.client.post('/logout/?next=http://evil/', follow=True)
        final_url = response.redirect_chain[-1][0]
        expected_url = settings.LOGOUT_REDIRECT_URL

        try:
            assert final_url == expected_url, "Unexpected final redirect URL after logout."
        except AssertionError as e:
            print_stacktrace(e)
            raise


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


if __name__ == '__main__':
    # Prepare the Django application
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', __name__)
    django_app = get_wsgi_application()

    # Running the test case
    try:
        test_case = LogoutRedirectTestCase()
        test_case.setUp()
        test_case.test_logout_redirect()
    except AssertionError:
        sys.exit(1)
    else:
        print("No issue detected.")
        sys.exit(0)
```