Here is the reproducer script:

```python
from django.urls import path, re_path
from django.urls.converters import int_converter

def to_url(pattern):
    if pattern.regex.match('non-matching-string'):
        return ''
    else:
        return 'wrong-path'

class Converter(int_converter):
    regex = re.compile(r'\d+')

def main():
    try:
        url = to_url(path('export/<foo:obj>/', name='export'))
        assert not bool(url)
    except AssertionError as e:
        print_stacktrace(e)
        raise SystemExit(1)

if __name__ == '__main__':
    main()
```

This script defines a Django URL converter and uses it in the `to_url` function. The `to_url` function is then used to test if an empty string is returned when the pattern does not match, which should raise an assertion error if the issue is present.

Please note that this script requires Django to be installed and available on your Python path.