Here is the `reproducer.py` file to reproduce the issue:
```
import os
import sys
from django.conf import settings
from django.core.management import execute_from_command_line
from django.db import models
from django.test.utils import get_runner

settings.configure(
    INSTALLED_APPS=['app'],
    DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': ':memory:'}},
)

class Bar(models.Model):
    pass

class Foo(models.Model):
    bar = models.ManyToManyField('Bar', blank=True)

def create_migrations():
    os.makedirs('app/migrations', exist_ok=True)
    execute_from_command_line(['manage.py', 'makemigrations', 'app'])
    execute_from_command_line(['manage.py', 'migrate'])

def change_model_and_migrate():
    global Bar, Foo
    class Bar(models.Model):
        pass
    class Foo(models.Model):
        bar = models.ManyToManyField('Foo', blank=True)
    create_migrations()

def test_admin_page():
    from django.test.client import RequestFactory
    from django.contrib.admin.sites import AdminSite
    from app.models import Foo
    admin.site.register(Foo, FooAdmin)

    class FooAdmin:
        pass

    factory = RequestFactory()
    request = factory.get('/admin/app/foo/add/')
    request.user = get_admin_user()

    def get_admin_user():
        from django.contrib.auth.models import User
        user = User(username='admin', is_superuser=True, is_staff=True)
        user.set_password('password')
        user.save()
        return user

    try:
        admin.site.each_request(request)
        response = FooAdmin(Foo, admin.site).add_view(request)
        assert response.status_code == 200
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue is present")

create_migrations()
change_model_and_migrate()
test_admin_page()

print("Issue is fixed")
sys.exit(0)

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
```
This script creates the models, runs the migrations, changes the model to use a self-referential ManyToManyField, and then tests the admin page. If an OperationalError occurs, it prints the stack trace and raises an AssertionError. If no exception occurs, it prints "Issue is fixed" and exits with code 0.