import os
from django.template import Template, Context
from django.conf import settings

settings.configure(INSTALLED_APPS=['django.contrib.admin'], TEMPLATES=[{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [],
    'APP_DIRS': True,
}])

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
    tmpl = Template('{% include var %}')
    ctx = Context({'var': ['admin/base.html', 'admin/fail.html']})
    tmpl.render(ctx)
except Exception as e:
    if isinstance(e, LookupError) and "TemplateDoesNotExist" in str(e):
        print_stacktrace(e)
        os._exit(0)
    else:
        print_stacktrace(e)
        raise AssertionError("Expected TemplateDoesNotExist exception, but got {}".format(type(e).__name__))
