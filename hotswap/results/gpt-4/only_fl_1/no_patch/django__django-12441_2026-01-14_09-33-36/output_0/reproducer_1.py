# reproducer.py

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
    import django
    from django import forms
    from django.conf import settings

    settings.configure(DEBUG=True, SECRET_KEY='thisisasecretkey', DATABASES={"default": {"ENGINE": "django.db.backends.sqlite3"}})
    django.setup()

    class TestForm(forms.Form):
        hidden_input = forms.CharField(widget=forms.HiddenInput)

        def clean(self):
            self.add_error(None, 'Form error')
            self.add_error('hidden_input', 'Hidden input error')
            super().clean()

    test_form = TestForm({})

    # Validate the form to ensure _errors is populated
    test_form.is_valid()
    
    # Record NON_FIELD_ERRORS before generating output
    initial_non_field_errors = list(test_form.non_field_errors())

    # Generate form HTML output twice to trigger issue
    test_form.as_p()
    test_form.as_p()

    # Record NON_FIELD_ERRORS after generating output
    final_non_field_errors = list(test_form.non_field_errors())

    try:
        assert initial_non_field_errors == final_non_field_errors, "NON_FIELD_ERRORS altered after rendering output."
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    main()
