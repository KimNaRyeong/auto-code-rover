Here is the reproducer script:

```python
import os
import django
from django.core.wsgi import get_wsgi_application
from django.conf import settings
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import HttpResponseForbidden
from django.views.decorators.csrf import ensure_csrf_cookie

app_dir = 'csrfbug'
os.chdir(app_dir)

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
            'DIRS': [os.path.join(app_dir, 'templates')],
            'APP_DIRS': True,
            'OPTIONS': {'debug': settings.DEBUG},
        }
    ]
)

app = get_wsgi_application()

User.objects.create_superuser('admin', 'admin@example.com', 'password')

def upload_file():
    file_path = os.path.join(settings.MEDIA_ROOT, 'test.txt')
    with open(file_path, 'w') as f:
        f.write('Test content')
    return SimpleUploadedFile('test.txt', b'Test content')

try:
    response = app.get('/admin/app/file/add/')
    response = app.post('/admin/app/file/add/', {'csrfmiddlewaretoken': '', 'file': upload_file()})
    if response.status_code == 403:
        print_stacktrace(response['exception'])
        raise AssertionError('CSRF failure incorrectly reported on upload when there is a problem with storage')
except Exception as e:
    print_stacktrace(e)
    exit(1)

print('Issue not reproduced, exiting with code 0')
exit(0)
```

This script sets up the Django environment, creates a superuser, and then attempts to upload a file. If the CSRF failure is reported for all file uploads (Scenario 3), it prints the stack trace of the issue and raises an `AssertionError`.