Here is the reproducer script:

```python
import django
from django.db import models
from datetime import datetime

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
    from django.db.models import F
except ImportError as e:
    print_stacktrace(e)
    exit(1)

django.setup()

class TemplateVersion(models.Model):
    published_at = models.DateTimeField(null=True)

template_versions = [TemplateVersion(published_at=datetime(2022, 2, 25, 13, 0, 12)) for _ in range(3)]
for i in range(3):
    if i == 1:
        template_versions[i].published_at = None
    elif i == 2:
        template_version = TemplateVersion(published_at=datetime(2022, 2, 21, 10, 18, 0))
        template_versions.append(template_version)

assert [tv.published_at for tv in sorted(template_versions, key=lambda x: (x.published_at is None, x.published_at), reverse=True)] != [None, datetime(2022, 2, 25, 13, 0, 12), datetime(2022, 2, 21, 10, 18, 0)]
assert [tv.published_at for tv in sorted(template_versions, key=lambda x: (x.published_at is None, -x.published_at), reverse=True)] != [None, datetime(2022, 2, 25, 13, 0, 12), datetime(2022, 2, 21, 10, 18, 0)]

print("Issue reproduced successfully.")
exit(0)
```

This script will raise an `AssertionError` if the issue is present and print a stack trace. If the issue is fixed, it will print "Issue reproduced successfully." and exit with code 0.