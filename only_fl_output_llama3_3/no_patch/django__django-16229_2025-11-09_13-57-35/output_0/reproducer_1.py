import os
from django.contrib import admin
from django.db import models
from django.forms.models import ModelForm, BaseModelFormSet
from django.forms.utils import ValidationError

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

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'testbed.settings')
    try:
        from django.core.wsgi import get_wsgi_application
        application = get_wsgi_application()
    except ImportError as e:
        print_stacktrace(e)
        raise AssertionError("Django not installed")

    admin.site.register(models.Model)

    class Thing(models.Model):
        pass

    class RelatedModel(models.Model):
        thing = models.ForeignKey(Thing, on_delete=models.CASCADE)
        plop = models.CharField(max_length=42)

    class RelatedModelForm(ModelForm):
        def clean(self):
            raise ValidationError("whatever")

    class RelatedModelInline(admin.TabularInline):
        form = RelatedModelForm
        model = RelatedModel
        extra = 1

    admin.site.register(Thing, ThingAdmin=admin.ModelAdmin)
    admin.site.register(RelatedModel)

    thing = Thing()
    try:
        thing.save()
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue not fixed")

if __name__ == "__main__":
    main()
