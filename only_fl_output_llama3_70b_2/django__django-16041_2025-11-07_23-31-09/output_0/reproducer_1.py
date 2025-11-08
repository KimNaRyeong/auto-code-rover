import os
import sys
from django.conf import settings
from django.test.utils import setup_test_environment
from django.core.management import execute_from_command_line

settings.configure(
    DEBUG=True,
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:'
        }
    },
    INSTALLED_APPS=[
        'my_app'
    ],
    TEMPLATES=[
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [],
            'APP_DIRS': True,
            'OPTIONS': {
                # ... some options here ...
            },
        },
    ]
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
    from django import setup
    setup()

    from my_app.models import MyModel

    class MyModel(models.Model):
        a_field = models.CharField(max_length=255)

    from django.forms.models import modelformset_factory
    from django.shortcuts import render
    from django.template.loader import get_template_from_string

    template_str = """
    {% extends "my_app/base.html" %}
    {% block content %}
    <form id="my-form" method="post">
     {% csrf_token %}
     {{ formset }}
     <input type="submit" value="Save">
    </form>
    {{ formset.empty_form }}
    {% endblock %}
    """

    template = get_template_from_string(template_str)

    MyModel(a_field='').save()

    FormSet = modelformset_factory(MyModel, fields=['a_field'], form_kwargs={'empty_permitted': True})

    context = {'formset': FormSet(queryset=MyModel.objects.none())}

    rendered_template = template.render(context)
    assert 'empty_form' in rendered_template
except Exception as e:
    print_stacktrace(e)
    raise AssertionError("Issue is present")
else:
    sys.exit(0)
