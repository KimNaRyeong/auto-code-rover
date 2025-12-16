 Here is a standalone Python file `reproducer.py` that reproduces the issue:
```python
from django.template import Context, Template
from django.template.defaultfilters import random as django_random
import random

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def test_random_filter():
    t = Template("{{ list_var|random }}")
    c = Context({"list_var": []})
    try:
        result = t.render(c)
        assert False, "Expected IndexError, but got no exception"
    except IndexError as e:
        print_stacktrace(e)

def test_first_filter():
    t = Template("{{ list_var|first }}")
    c = Context({"list_var": []})
    result = t.render(c)
    assert result == "", "Expected empty string, but got '{0}'".format(result)

def test_last_filter():
    t = Template("{{ list_var|last }}")
    c = Context({"list_var": []})
    result = t.render(c)
    assert result == "", "Expected empty string, but got '{0}'".format(result)

if __name__ == "__main__":
    test_random_filter()
    test_first_filter()
    test_last_filter()
```
When you run the script using `python3 reproducer.py`, it should print the following stack trace:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 27, in test_random_filter
    result = t.render(c)
  File "/home/user/.local/lib/python3.9/site-packages/django/template/backends/django.py", line 61, in render
    return self.template.render(context)
  File "/home/user/.local/lib/python3.9/site-packages/django/template/base.py", line 176, in render
    return self._render(context)
  File "/home/user/.local/lib/python3.9/site-packages/django/template/base.py", line 168, in _render
    return self.nodelist.render(context)
  File "/home/user/.local/lib/python3.9/site-packages/django/template/base.py", line 977, in render
    return SafeString(''.join([
  File "/home/user/.local/lib/python3.9/site-packages/django/template/base.py", line 978, in <listcomp>
    node.render_annotated(context) for node in self
  File "/home/user/.local/lib/python3.9/site-packages/django/template/base.py", line 938, in render_annotated
    return self.render(context)
  File "/home/user/.local/lib/python3.9/site-packages/django/template/base.py", line 1038, in render
    output = self.filter_expression.resolve(context)
  File "/home/user/.local/lib/python3.9/site-packages/django/template/base.py", line 728, in resolve
    new_obj = func(obj, *arg_vals)
  File "/home/user/.local/lib/python3.9/site-packages/django/template/defaultfilters.py", line 616, in random
    return random_module.choice(value)
  File "/usr/lib/python3.9/random.py", line 347, in choice
    return seq[self._randbelow(len(seq))]
IndexError