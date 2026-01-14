 Here is a standalone Python script `reproducer.py` that reproduces the issue:
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
    expected_result_1 = [
        None,
        datetime.datetime(2022, 2, 25, 13, 0, 12, 91916, tzinfo=<UTC>),
        datetime.datetime(2022, 2, 21, 10, 18, 0, 169248, tzinfo=<UTC>),
    ]
    actual_result_1 = [tv.published_at for tv in TemplateVersion.objects.order_by(F("published_at").desc(nulls_first=True))]
    if actual_result_1 != expected_result_1:
        raise AssertionError(f"Expected {expected_result_1}, but got {actual_result_1}")

    expected_result_2 = [
        None,
        datetime.datetime(2022, 2, 25, 13, 0, 12, 91916, tzinfo=<UTC>),
        datetime.datetime(2022, 2, 21, 10, 18, 0, 169248, tzinfo=<UTC>),
    ]
    actual_result_2 = [tv.published_at for tv in TemplateVersion.objects.order_by(F("published_at").desc(nulls_first=False))]
    if actual_result_2 != expected_result_2:
        raise AssertionError(f"Expected {expected_result_2}, but got {actual_result_2}")

    expected_result_3 = [
        datetime.datetime(2022, 2, 25, 13, 0, 12, 91916, tzinfo=<UTC>),
        datetime.datetime(2022, 2, 21, 10, 18, 0, 169248, tzinfo=<UTC>),
        None,
    ]
    actual_result_3 = [tv.published_at for tv in TemplateVersion.objects.order_by(F("published_at").desc(nulls_last=True))]
    if actual_result_3 != expected_result_3:
        raise AssertionError(f"Expected {expected_result_3}, but got {actual_result_3}")

    expected_result_4 = [
        None,
        datetime.datetime(2022, 2, 25, 13, 0, 12, 91916, tzinfo=<UTC>),
        datetime.datetime(2022, 2, 21, 10, 18, 0, 169248, tzinfo=<UTC>),
    ]
    actual_result_4 = [tv.published_at for tv in TemplateVersion.objects.order_by(F("published_at").desc(nulls_last=False))]
    if actual_result_4 != expected_result_4:
        raise AssertionError(f"Expected {expected_result_4}, but got {actual_result_4}")

if __name__ == "__main__":
    try:
        test_ordering()
        print("No issues found.")
        sys.exit(0)
    except AssertionError as e:
        print_stacktrace(e)
        sys.