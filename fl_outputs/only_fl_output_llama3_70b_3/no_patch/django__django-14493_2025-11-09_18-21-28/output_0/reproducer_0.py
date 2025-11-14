import os
import sys
from django.conf import settings
from django.core.management import call_command
from django.contrib.staticfiles.storage import ManifestStaticFilesStorage

class MyManifestStaticFilesStorage(ManifestStaticFilesStorage):
    max_post_process_passes = 0

settings.configure(
    STATICFILES_STORAGE='__main__.MyManifestStaticFilesStorage',
)

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

try:
    call_command('collectstatic', verbosity=0, interactive=False)
except Exception as e:
    print_stacktrace(e)
    assert isinstance(e, UnboundLocalError), "Expected UnboundLocalError"
    sys.exit(1)

sys.exit(0)
