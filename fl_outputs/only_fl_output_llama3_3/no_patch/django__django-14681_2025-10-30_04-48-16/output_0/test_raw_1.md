Here is the reproducer script:

```python
import os
import django
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import HttpResponseForbidden
from django.views.decorators.csrf import ensure_csrf_cookie
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

def reproducer():
    os.chdir('csrfbug')
    settings.configure(
        DEBUG=True,
        SECRET_KEY='secret_key',
        ROOT_URLCONF=__name__,
        MIDDLEWARE=[
            'django.middleware.common.CommonMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware'
        ],
        TEMPLATES=[
            {
                'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'DIRS': [os.path.join('csrfbug', 'templates')],
                'APP_DIRS': True,
                'OPTIONS': {'debug': settings.DEBUG},
            }
        ]
    )

    try:
        from django.contrib.auth.models import User
        from .models import File

        app = get_wsgi_application()

        User.objects.create_superuser('admin', 'admin@example.com', 'password')

        response = app.get('/admin/app/file/add/')
        response = app.post('/admin/app/file/add/', {'csrfmiddlewaretoken': '', 'file': SimpleUploadedFile('test.txt', b'Test content')})
        if response.status_code == 403:
            print_stacktrace(response['exception'])
            raise AssertionError('CSRF failure incorrectly reported on upload when there is a problem with storage')
    except Exception as e:
        print_stacktrace(e)
        exit(1)

    print('Issue not reproduced, exiting with code 0')
    exit(0)

if __name__ == '__main__':
    reproducer()
```

This script sets up the Django environment, creates a superuser, and then attempts to upload a file. If the CSRF failure is reported for all file uploads (Scenario 3), it prints the stack trace of the issue and raises an `AssertionError`.