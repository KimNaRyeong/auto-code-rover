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

# Ensures Django is setup correctly for script running outside the context of a project.
def setup_django_environment():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "__main__")
    import django
    from django.conf import settings

    settings.configure(
        DEBUG=True,
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": ":memory:",
            }
        },
        ROOT_URLCONF="__main__",
        INSTALLED_APPS=[
            "django.contrib.admin",
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "django.contrib.sessions",
            "django.contrib.messages",
            "django.contrib.staticfiles",
        ],
        SECRET_KEY="not_so_secret",
        STATIC_URL="/static/",
        STATIC_ROOT="staticfiles",
        STATICFILES_STORAGE="__main__.MyManifestStaticFilesStorage",
        TEMPLATES=[
            {
                "BACKEND": "django.template.backends.django.DjangoTemplates",
                "DIRS": [],
                "APP_DIRS": True,
            }
        ],
        USE_TZ=True,
    )

    django.setup()

from django.contrib.staticfiles.storage import ManifestStaticFilesStorage
from django.core.management import call_command

class MyManifestStaticFilesStorage(ManifestStaticFilesStorage):
    max_post_process_passes = 0

def run_collectstatic():
    try:
        # Ensure the STATIC_ROOT exists
        os.makedirs("staticfiles", exist_ok=True)
        call_command("collectstatic", interactive=False, verbosity=0, clear=True)
        print("The issue has been resolved.")
        sys.exit(0)
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("The issue is present.") from e

if __name__ == "__main__":
    setup_django_environment()
    run_collectstatic()
