import os
import django
from django.db import models
from django.db.models.functions import Lag
from django.db.models import Window, F

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
    from test1.models import LagTest
    w = Window(expression=Lag('amount',7), partition_by=[F('modified')], order_by=F('modified').asc())
    q = LagTest.objects.all().annotate(w=w)
    print(q)
except Exception as e:
    print_stacktrace(e)
    raise AssertionError("Issue not fixed")
