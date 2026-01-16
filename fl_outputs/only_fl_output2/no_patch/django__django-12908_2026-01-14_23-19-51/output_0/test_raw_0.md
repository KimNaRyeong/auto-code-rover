```python
# reproducer.py

import django
from django.db import models
from django.db.models import Value, IntegerField
from django.conf import settings
from django.core.management import execute_from_command_line
import os
import sys

settings.configure(
    DEBUG=True,
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'db.sqlite3',
        }
    },
    INSTALLED_APPS=('__main__',),
    USE_TZ=True,
)

django.setup()


class Sample(models.Model):
    name = models.CharField(max_length=30)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    class Meta:
        app_label = '__main__'


class Reproducer:
    @staticmethod
    def setup_database():
        if not os.path.exists('db.sqlite3'):
            execute_from_command_line(['manage.py', 'migrate'])

    def get_or_create_admin_user(self):
        from django.contrib.auth.models import User
        user, _ = User.objects.get_or_create(username='admin')
        return user

    @staticmethod
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

    def test_union_annotated_diff_distinct(self):
        try:
            user = self.get_or_create_admin_user()
            Sample.objects.bulk_create([
                Sample(user=user, name="Sam1"),
                Sample(user=user, name="Sam2 acid"),
                Sample(user=user, name="Sam3"),
                Sample(user=user, name="Sam4 acid"),
                Sample(user=user, name="Dub"),
                Sample(user=user, name="Dub"),
                Sample(user=user, name="Dub"),
            ])

            qs = Sample.objects.filter(user=user)
            qs1 = qs.filter(name='Dub').annotate(rank=Value(0, IntegerField()))
            qs2 = qs.filter(name='Sam1').annotate(rank=Value(1, IntegerField()))
            qs = qs1.union(qs2)
            qs = qs.order_by('name').distinct('name')  # THIS DISTINCT DOESN'T THROW ERROR BUT IT SHOULD
            assert qs.count() == 2, "Distinct on union queryset did not work as expected."
        except AssertionError as e:
            self.print_stacktrace(e)
            sys.exit(1)
        print("Issue not present, test passed.")
        sys.exit(0)


if __name__ == "__main__":
    Reproducer.setup_database()
    tester = Reproducer()
    tester.test_union_annotated_diff_distinct()
```