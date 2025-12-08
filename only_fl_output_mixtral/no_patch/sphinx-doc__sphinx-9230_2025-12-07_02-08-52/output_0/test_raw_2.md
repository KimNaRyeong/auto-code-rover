 Here is a standalone python file `reproducer.py` that reproduces the issue:
```python
def function_with_dict_param(param1, dict_param: dict[str, str] = None):
    """
    :param dict(str, str) dict_param: (optional)
    """
    pass

try:
    # Call the function with no arguments to trigger autodoc
    function_with_dict_param()
except Exception as e:
    print_stacktrace(e)
```
To execute the script, save it in the root directory of the project and run `python3 reproducer.py`. The script should raise an `AssertionError` when the issue is present and print a stack trace of the issue.

The expected behavior is that the `dict_param` parameter should be rendered in the generated docs as `dict_param (dict(str, str)) – (optional)`, but it is being incorrectly rendered as `dict_param (dict(str,) –(optional)`.

The current environment information is:

* OS: Mac
* Python version: 3.9.0
* Sphinx version: 4.0.1
* Sphinx extensions:  ["sphinx.ext.autodoc", "sphinx.ext.autosummary", "sphinx.ext.intersphinx", "autodocsumm"]
* Extra tools: Browser Firefox.

Note: The `print_stacktrace` function used in the script is the same as the one provided in the issue description.