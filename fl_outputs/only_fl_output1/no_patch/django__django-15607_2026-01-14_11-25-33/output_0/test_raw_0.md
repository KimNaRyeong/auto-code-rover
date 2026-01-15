```python
# reproducer.py
from django.contrib.auth.models import User
from django.contrib.auth.views import LogoutView
from django.http import HttpResponse
from django.test import Client, TestCase
from django.urls import path
from django.conf import settings

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

def logout_view(request):
    return LogoutView.as_view()(request)

urlpatterns = [
    path('logout/', logout_view, name='logout'),
]

class LogoutRedirectTestCase(TestCase):
    def setUp(self):
        # Setup URL patterns
        settings.ROOT_URLCONF = __name__
        # Set LOGOUT_REDIRECT_URL
        settings.LOGOUT_REDIRECT_URL = '/redirected_successfully/'
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client = Client()

    def test_unnecessary_redirect(self):
        try:
            self.client.login(username='testuser', password='12345')
            response = self.client.post('/logout/?next=http://evil/', follow=True)
            # Check that we are redirected directly to LOGOUT_REDIRECT_URL without unnecessary intermediaries
            final_redirect = response.redirect_chain[-1] if response.redirect_chain else ('', '')
            assert final_redirect[0] == settings.LOGOUT_REDIRECT_URL, "The logout did not correctly redirect to LOGOUT_REDIRECT_URL"
            assert len(response.redirect_chain) == 1, "There was an unnecessary intermediary redirect"
        except AssertionError as e:
            print_stacktrace(e)
            raise

if __name__ == '__main__':
    import django
    from django.conf import settings

    settings.configure(
        INSTALLED_APPS=[
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
        ],
        MIDDLEWARE=[
            'django.middleware.security.SecurityMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.middleware.common.CommonMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
            'django.middleware.clickjacking.XFrameOptionsMiddleware',
        ],
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': 'mydatabase',
            }
        },
        SECRET_KEY='REPLACE_ME',
    )

    django.setup()
    from django.test.runner import DiscoverRunner

    test_runner = DiscoverRunner()
    test_suite = LogoutRedirectTestCase(methodName='test_unnecessary_redirect')
    result = test_runner.run_suite(test_suite)
    if result.wasSuccessful():
        print("Test passed, no unnecessary redirects.")
        exit(0)
    else:
        exit(1)
```

This script sets up a minimal Django environment including a basic user model, session, and authentication system required to test the logout functionality. It modifies `settings` on the fly because it's designed to run standalone, outside of a Django project structure.

It programmatically logs in a user, posts to the logout URL with a next parameter pointing to an external URL, and then checks the final URL the user is redirected to. The expected behavior, according to the issue description, is to ignore the `next` parameter and redirect directly to `LOGOUT_REDIRECT_URL` without any intermediate redirects. If the unnecessary redirect occurs, the script uses `print_stacktrace` to print a detailed error stack trace and exits with code 1, indicating the presence of the issue. If the issue is not present, it exits with code 0, indicating success.