 I apologize for the mistake in my previous response. Here is the corrected `reproducer.py` script that reproduces the issue:
```python
from django.db.models import F
from myapp.models import TemplateVersion

def print_stacktrace(e: Exception):
    import traceback    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def test_ordering():
    published_ats_nulls_first_true = [
        tv.published_at for tv in TemplateVersion.objects.order_by(F("published_at").desc(nulls_first=True))
    ]
    published_ats_nulls_first_false = [
        tv.published_at for tv in TemplateVersion.objects.order_by(F("published_at").desc(nulls_first=False))
    ]
    published_ats_nulls_last_true = [
        tv.published_at for tv in TemplateVersion.objects.order_by(F("published_at").desc(nulls_last=True))
    ]
    published_ats_nulls_last_false = [
        tv.published_at for tv in TemplateVersion.objects.order_by(F("published_at").desc(nulls_last=False))
    ]

    expected_published_ats_nulls_first_true = [
        None,
        datetime.datetime(2