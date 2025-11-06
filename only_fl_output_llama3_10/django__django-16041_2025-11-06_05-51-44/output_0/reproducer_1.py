from django.db.models import Model
from django.forms.models import modelformset_factory
from django.template.loader import get_template
from django.template.response import TemplateResponse
from django.urls.resolvers import URLResolver
import sys
import traceback

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def main():
    try:
        class MyModel(Model):
            pass

        formset = modelformset_factory(MyModel, fields=['a_field'])
        template = get_template('my_app/my_model_formset.html')
        context = {'formset': formset(queryset=MyModel.objects.none(), form_kwargs={'empty_permitted': True})}
        TemplateResponse(request=None, template_name='my_app/my_model_formset.html', context=context).render()
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue not fixed")

if __name__ == "__main__":
    main()
