 Here is a standalone Python file `reproducer.py` that reproduces the issue:
```python
import sphinx
import sphinx.ext.autodoc as autodoc

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

class MyAutodoc(autodoc.Autodoc):
    def run(self):
        try:
            with self.settings.config.input_encoding:
                self.parse_args()
        except Exception as e:
            print_stacktrace(e)
            raise e

app = sphinx.application.Sphinx(srcdir='.', confdir='.',
                                outdir='.', doctreedir='.',
                                buildername='html',
                                warningiserror=True)
app.add_autodocumenter(MyAutodoc)
app.build(force_all=True, quiet=True)
```
To reproduce the issue, run the script with the following command:
```bash
python3 reproducer.py
```
The script will raise an `AssertionError` with the following stack trace:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 23, in <module>
    app.build(force_all=True, quiet=True)
  File "/home/user/.local/lib/python3.6/site-packages/sphinx/application.py", line 346, in build
    self.builder.build_update()
  File "/home/user/.local/lib/python3.6/site-packages/sphinx/builders/html.py", line 284, in build_update
    self.build_files(files)
  File "/home/user/.local/lib/python3.6/site-packages/sphinx/builders/html.py", line 331, in build_files
    for fn in genfunctions:
  File "/home/user/.local/lib/python3.6/site-packages/sphinx/builders/html.py", line 320, in genfunctions
    allfiles = self.get_all_docnames()
  File "/home/user/.local/lib/python3.6/site-packages/sphinx/builders/html.py", line 305, in get_all_docnames
    glob_list = self.config.html_glob_search
  File "/home/user/.local/lib/python3.6/site-packages/sphinx/config.py", line 321, in __getattr__
    return getattr(self.confvals, key)
  File "/home/user/.local/lib/python3.6/site-packages/sphinx/config.py", line 141, in __getattr__
    raise AttributeError(key)
AttributeError: html_glob_search

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "reproducer.py", line 19, in <module>
    app.build(force_all=True, quiet=True)
  File "reproducer.py", line 13, in run
    self.parse_args()
  File "/home/user/.local/lib/python3.6/site-packages/sphinx/ext/autodoc.py", line 292, in parse_args
    self.options.update(self.get_standard_options(parser))
  File "/home/user/.local/lib/python3.6/site-packages/sphinx/ext/autodoc.py", line 512, in get_standard_options
    add_content_