import os
import django
from django.conf import settings
from django.test.utils import override_settings
from django.template.loader import get_template
from django.template import Context, Template
from django.core.exceptions import AssertionError

settings.configure()

os.environ['DJANGO_SETTINGS_MODULE'] = 'my_app.settings'

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

def reproduce_issue():
    from django.forms.models import modelformset_factory
    from django.db.models import Model

    class MyModel(Model):
        def __str__(self):
            return "MyModel"

    ff = modelformset_factory(MyModel, fields=['a_field'])

    template = get_template('my_model_formset.html')
    context = Context({
        'formset': ff(queryset=MyModel.objects.none(), form_kwargs={'empty_permitted': True})
    })

    try:
        template.render(context)
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue reproduced")

if __name__ == "__main__":
    reproduce_issue()
