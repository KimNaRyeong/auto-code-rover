import django
from django.template import Context, Template
from django.conf import settings

def setup_django_environment():
    settings.configure(
        TEMPLATES=[
            {
                'BACKEND': 'django.template.backends.django.DjangoTemplates',
            }
        ]
    )
    django.setup()

def render_template_with_empty_list():
    template = Template("{{ list_var|random }}")
    context = Context({"list_var": []})
    return template.render(context)

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

def test_random_filter_with_empty_list():
    setup_django_environment()
    try:
        output = render_template_with_empty_list()
        assert output == "", "The 'random' filter did not return an empty string for an empty list."
        print("Test passed: The 'random' filter returned an empty string for an empty list.")
    except Exception as e:
        print_stacktrace(e)
        assert False, "The 'random' filter raised an exception for an empty list."

if __name__ == "__main__":
    test_random_filter_with_empty_list()
