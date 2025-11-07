import os
import django
from django.conf import settings
from django.db import models
from django.db.models import Case, When, Value, Exists, OuterRef, Q

# Setup Django environment
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
settings.configure(
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    },
    INSTALLED_APPS=[
        '__main__',  # This scripts acts as its own Django app
    ],
    USE_TZ=True,
)
django.setup()

# Define models
class State(models.Model):
    pass

class County(models.Model):
    name = models.CharField(max_length=50)
    state = models.ForeignKey(State, related_name='counties', on_delete=models.CASCADE)

# Apply migrations (required for SQLite backend)
from django.core.management import call_command
call_command('migrate', run_syncdb=True)

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

def run_test():
    try:
        # Attempt to use Exist expression with When without wrapping it with Q object (expected to fail as per issue description)
        County.objects.annotate(
            status=Case(
                When(Exists(State.objects.filter(counties=OuterRef('pk'), name="Texas")), name="Dallas", then=Value("DALLAS COUNTY")),
                default=Value("ELSEWHERE"),
            )
        )
        raise AssertionError("Issue NOT reproduced - Expected a TypeError.")
    except TypeError as e:
        try:
            # Attempt to use Exist expression with When wrapped with Q object
            County.objects.annotate(
                status=Case(
                    When(Q(Exists(State.objects.filter(counties=OuterRef('pk'), name="Texas")), name="Dallas"), then=Value("DALLAS COUNTY")),
                    default=Value("ELSEWHERE"),
                )
            )
            print("Issue reproduced successfully. TypeError was raised as expected.")
        except Exception as e_inner:
            raise AssertionError("Unexpected exception was raised during the reproduction process.") from e_inner
    except Exception as e_not_type_error:
        print_stacktrace(e_not_type_error)
        raise AssertionError("Unexpected exception type during test run.") from e_not_type_error

if __name__ == "__main__":
    run_test()
