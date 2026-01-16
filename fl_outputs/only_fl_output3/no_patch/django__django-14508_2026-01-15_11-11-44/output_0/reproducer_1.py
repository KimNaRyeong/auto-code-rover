# reproducer.py
import os
import sys


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


def setup_django_environment():
    from django.conf import settings
    settings.configure(
        DEBUG=True,
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': os.path.join(os.getcwd(), 'db.sqlite3'),
            }
        },
        INSTALLED_APPS=(
            '__main__',
        ),
        USE_I18N=True,
        USE_L10N=True,
        USE_TZ=True,
    )
    import django
    django.setup()


def define_models():
    from django.db import models

    class SomeTestModel(models.Model):
        some_field = models.CharField(max_length=100)

        class Meta:
            abstract = True

        @property
        def other_field(self):
            return "[OTHER] %s" % self.some_field

    class OtherModel(SomeTestModel):
        other_field = models.CharField(max_length=100)

    class AndMoreOther(SomeTestModel):
        not_important_field = models.CharField(max_length=100)

    return OtherModel


def main():
    setup_django_environment()
    OtherModel = define_models()
    try:
        o = OtherModel()
    except AttributeError as e:
        print_stacktrace(e)
        raise AssertionError("Issue is present") from None
    else:
        print("The issue has been resolved.")


if __name__ == '__main__':
    main()
