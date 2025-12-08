 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
from django.urls import replace_named_groups
from django.utils.regex_ captures import simplify_regexp

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def simplify_regexp_test():
    urlpattern = r'entries/(?P<pk>[^/.]+)/relationships/(?P<related_field>\w+)'
    simplified_pattern = simplify_regexp(urlpattern)
    print(simplified_pattern)
    assert simplified_pattern == r'entries/<pk:pk>/relationships/<related_field:\w+>'

def replace_named_groups_test():
    urlpattern = r'entries/(?P<pk>[^/.]+)/relationships/(?P<related_field>\w+)'
    to_replace = {'pk': '123', 'related_field': 'author'}
    replaced_pattern = replace_named_groups(urlpattern, **to_replace)
    print(replaced_pattern)
    assert replaced_pattern == r'entries/123/relationships/author'

def main():
    simplify_regexp_test()
    replace_named_groups_test()

if __name__ == '__main__':
    try:
        main()
    except AssertionError as e:
        print_stacktrace(e)
        raise
```
To run the script, execute `python3 reproducer.py` in the terminal. The script will print the simplified and replaced regular expressions and raise an `AssertionError` with a stack trace if the issue is present. If the issue is fixed, the script will exit with code 0 without printing any error messages.