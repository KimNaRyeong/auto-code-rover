```python
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

def test_random_filter_with_empty_list():
    from django.template import Template, Context
    from django.conf import settings
    
    # Basic Django setup
    settings.configure()
    
    empty_list_template_str = '{% load custom_tags %}{{ list_var|random }}'
    t = Template(empty_list_template_str)
    c = Context({"list_var": []})
    
    try:
        rendered = t.render(c)
        # We expect it to not raise an exception and hence reach this line.
        # Since there're no elements to choose from, it either needs to return an empty string or behave gracefully.
        assert rendered == '', "The 'random' filter did not handle an empty list gracefully."
    except Exception as e:
        print_stacktrace(e)
        # If an AssertionError is not raised, but any other exception is,
        # it means the issue is present as the 'random' filter crashed/failed.
        raise AssertionError("The 'random' filter failed with an empty list.")

if __name__ == '__main__':
    try:
        test_random_filter_with_empty_list()
    except AssertionError as e:
        print(e)
        exit(1) # Exit with an error code if the issue is present.
    print("Test passed. The issue is fixed.")
    exit(0) # Exit gracefully when the issue is fixed.
```