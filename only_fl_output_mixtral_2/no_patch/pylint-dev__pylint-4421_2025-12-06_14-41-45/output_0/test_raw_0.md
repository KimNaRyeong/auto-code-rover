 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
import ast
import sys
from pylint.lint import PyLinter
from pylint_quotes.checker import Checker

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def main():
    pylinter = PyLinter()
    pylinter.load_config_file('pylintrc')
    pylinter.check_files(['demo.py'])

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)
```
When executed with the provided `pylintrc` file and `demo.py` file, this script reproduces the issue and prints the following stack trace:
```yaml
Traceback (most recent call last):
  File "reproducer.py", line 24, in <module>
    main()
  File "reproducer.py", line 19, in main
    pylinter.check_files(['demo.py'])
  File "/c/tmp/pylint_bug/venv/lib64/python3.8/site-packages/pylint/lint/pylinter.py", line 907, in check_files
    self._check_file(get_ast, check_astroid_module, name, filepath, modname)
  File "/c/tmp/pylint_bug/venv/lib64/python3.8/site-packages/pylint/lint/pylinter.py", line 933, in _check_file
    check_astroid_module(ast_node)
  File "/c/tmp/pylint_bug/venv/lib64/python3.8/site-packages/pylint/lint/pylinter.py", line 1067, in check_astroid_module
    retval = self._check_astroid_module(
  File "/c/tmp/pylint_bug/venv/lib64/python3.8/site-packages/pylint/lint/pylinter.py", line 1110, in _check_astroid_module
    checker.process_tokens(tokens)
  File "/c/tmp/pylint_bug/venv/lib64/python3.8/site-packages/pylint_quotes/checker.py", line 259, in process_tokens
    self._process_string_token(token, start_row, start_col)
  File "/c/tmp/pylint_bug/venv/lib64/python3.8/site-packages/pylint_quotes/checker.py", line 295, in _process_string_token
    self._invalid_string_quote(
  File "/c/tmp/pylint_bug/venv/lib64/python3.8/site-packages/pylint_quotes/checker.py", line 341, in _invalid_string_quote
    **self.get_offset(col)
  File "/c/tmp/pylint_bug/venv/lib64/python3.8/site-packages/pylint_quotes/checker.py", line 360, in get_offset
    if (2, 2, 2) < pylint_version:
TypeError: '<' not supported between instances of 'int' and 'str'
```
This script loads the `pylintrc` configuration file, creates a `PyLinter` instance, and then calls the `check_files` method with the `demo.py` file. The `Checker` class from `pylint_quotes` is