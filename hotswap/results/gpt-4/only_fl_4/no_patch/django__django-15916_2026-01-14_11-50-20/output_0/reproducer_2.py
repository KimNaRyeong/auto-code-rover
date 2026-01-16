# reproducer.py
import sys

def print_stacktrace(e: Exception):
    import traceback
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def setup_django_environment():
    from django.conf import settings
    import django
    settings.configure(
        INSTALLED_APPS=[
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.admin',
        ],
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            },
        },
        USE_I18N=True,
        USE_L10N=True,
        USE_TZ=True,
        SECRET_KEY='django_tests_secret_key',
    )
    django.setup()

def run_test():
    from django import forms
    from django.db import models

    class MyModel(models.Model):
        active = models.BooleanField(default=False)
        name = models.CharField(max_length=64)

        class Meta:
            app_label = 'myapp'  # Required for models not defined in an application

    def all_required(field, **kwargs):
        formfield = field.formfield(**kwargs)
        if formfield:
            formfield.required = True
        return formfield

    class MyForm(forms.ModelForm):
        formfield_callback = all_required

        class Meta:
            model = MyModel
            fields = ['active', 'name']

    FactoryForm = forms.modelform_factory(MyModel, form=MyForm)

    # Test if the formfield_callback is correctly used
    test_form = FactoryForm()
    try:
        assert test_form.fields['active'].required, "Field 'active' should be required."
        assert test_form.fields['name'].required, "Field 'name' should be required."
        print("Success: All fields are marked as required as expected.")
        sys.exit(0)
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == "__main__":
    try:
        setup_django_environment()
        run_test()
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)
