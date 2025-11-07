```python
import os
import sys
from django.conf import settings
from django.core.management import execute_from_command_line

# Define settings for minimal Django project
settings.configure(
    DEBUG=True,
    SECRET_KEY='a-very-secret-key',
    ROOT_URLCONF=__name__,
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'your_db_name',
            'USER': 'your_db_user',
            'PASSWORD': 'your_db_password',
            'HOST': 'your_db_host',
            'PORT': 'your_db_port',
        }
    },
    INSTALLED_APPS=[
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.admin',
        'django.contrib.sessions',
        '__main__',  # This script is its own Django app
    ],
    MIDDLEWARE=[
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
    ],
)

from django.db import models
from django.contrib import admin
from django.http import HttpResponse

# Define models as per issue description
class User(models.Model):
    email = models.CharField(max_length=100)

class Post(models.Model):
    title = models.CharField(max_length=100)
    authors = models.ManyToManyField(User)

# Register models to admin
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    search_fields = ('title', 'authors__email')

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass

# Minimal views to trigger the crash
def index(request):
    # Attempting to reproduce the error by mimicking admin delete action
    try:
        post = Post.objects.create(title="Sample Post")
        user = User.objects.create(email="sample@email.com")
        post.authors.add(user)

        search_result = Post.objects.filter(title__startswith=post.title[:2])
        search_result.delete()

        return HttpResponse("No error occurred, unable to reproduce the issue.")
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue reproduced successfully!")

# Util function to print stack trace
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

# Handle 'runserver' command
from django.urls import path
urlpatterns = [
    path('', index),
]

if __name__ == '__main__':
    from django.core.management.commands.runserver import Command as runserver
    runserver.default_addr = "127.0.0.1"
    runserver.default_port = "8000"
    execute_from_command_line(sys.argv)
```

Please replace `'your_db_name'`, `'your_db_user'`, `'your_db_password'`, `'your_db_host'`, and `'your_db_port'` with the actual credentials of your PostgreSQL database.

To test, ensure you have Django and a PostgreSQL database ready. Then, place this script at the root of your Django project directory, and execute it using `python3 reproducerer.py runserver`. This script will set up a minimal Django app, including the models and admin configurations described in the issue. Then, it attempts to perform the actions leading to the error, and if the error is reproduced, its stack trace is printed using the provided `print_stacktrace` function, followed by an `AssertionError` to indicate the issue was successfully reproduced.