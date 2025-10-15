```python
# reproducer.py
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

def main():
    import os
    import sys
    import django
    from django.conf import settings
    from django.db import models

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    settings.configure(
        DATABASES = {
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
            }
        },
        INSTALLED_APPS = (
            "__main__",  # This registers the current file as an app.
        ),
        TIME_ZONE = "UTC",
    )

    django.setup()

    class Foo(models.Model):
        a = models.CharField(max_length=255)
        d = models.IntegerField()

    class Bar(models.Model):
        a = models.ForeignKey(Foo, on_delete=models.CASCADE)
        b = models.CharField(max_length=255)

    try:
        # Running migrations programmatically
        from django.core.management import call_command
        call_command('makemigrations', '__main__', interactive=False)
        call_command('migrate', interactive=False)

        import copy
        from django.test import TestCase

        class ForeignKeyCachingBehaviorTest(TestCase):
            def test_copy(self):
                foo1 = Foo.objects.create(a='foo1', d=1)
                foo2 = Foo.objects.create(a='foo2', d=2)
                bar1 = Bar.objects.create(a=foo1, b='bar1')
                bar2 = copy.copy(bar1)
                bar2.pk = None
                bar2.a = foo2
                # bar2 points to foo2
                self.assertEqual(bar2.a, foo2)
                self.assertEqual(bar2.a.id, bar2.a_id)
                # These fail on Django >= 2.0
                self.assertEqual(bar1.a, foo1)
                self.assertEqual(bar1.a.id, bar1.a_id)

        # Run the test
        test = ForeignKeyCachingBehaviorTest()
        test.setUp()
        test.test_copy()
        test.tearDown()

    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(2)
    
    print("Test passed, no issue detected.")
    sys.exit(0)

if __name__ == "__main__":
    main()
```

This is a standalone Python script named `reproducer.py` that demonstrates how to reproduce the reported issue in a Django model regarding foreign key (FK) field caching behavior change when transitioning from Django 1.11.x to Django 2.x. It dynamically configures Django settings and models for this specific test scenario, performs the test, and prints a stack trace if the `AssertionError` (representing the issue) is triggered. If the test passes (indicating that the issue is resolved or does not exist within the tested environment), the script exits normally (exit code 0).