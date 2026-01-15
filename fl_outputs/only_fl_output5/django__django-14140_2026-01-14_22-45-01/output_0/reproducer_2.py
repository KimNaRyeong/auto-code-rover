# reproducer.py
import django
from django.conf import settings

def setup_django():
    settings.configure(
        INSTALLED_APPS=[
            'django.contrib.auth',
            'django.contrib.contenttypes',
        ],
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            },
        },
        USE_TZ=True,
    )
    django.setup()

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

def test_deconstruct_q_with_non_subscriptable_child():
    from django.db.models import Q, Exists
    from django.contrib.auth import get_user_model
    
    try:
        user_exists = Exists(get_user_model().objects.filter(username='jim'))
        q = Q(user_exists)
        q.deconstruct()
        print("The issue seems to be fixed.")
        return True
    except TypeError as e:
        print_stacktrace(e)
        return False

if __name__ == "__main__":
    setup_django()
    if not test_deconstruct_q_with_non_subscriptable_child():
        raise AssertionError("The issue is present.")
