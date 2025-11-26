Here is the standalone Python file `reproducer.py` to reproduce the issue:
```
import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'reproducer.settings'

from django.conf import settings
from django.db import models

class Document(models.Model):
    pass

class Picking(Document):
    document_ptr = models.OneToOneField(Document, on_delete=models.CASCADE, parent_link=True, related_name='+')
    origin = models.OneToOneField(Document, related_name='picking', on_delete=models.PROTECT)

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
    models.get_app_config('reproducer').get_models()
except Exception as e:
    print_stacktrace(e)
    assert False, "Issue is present"
else:
    print("Issue is fixed")
    sys.exit(0)
```
<|start_header_id|><|start_header_id|>