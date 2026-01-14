 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
import sys
import sphinx
import sphinx_gallery

def print_stacktrace(e: Exception):
    import traceback    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def main():
    # Set up a dummy project
    sys.path.insert(0, '.')
    app = sphinx.application.Sphinx(srcdir='.', confdir='.', outdir='.')

    # Reproduce the issue
    try:
        app.setup_extension('sphinx_gallery.gen_gallery')
        assert app.extensions['sphinx_gallery'].needs_sphinx >= '4.0.0'
        assert app.extensions['sphinx_gallery'].needs_gallery_version >= '0.6.0'

        # This should not raise an exception
        app.setup_extension('sphinx_gallery.gen_gallery', version='0.10.0')

        print("The issue is not present.")
        sys.exit(0)
    except sphinx.errors.VersionRequirementError as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == '__main__':
    main()
```
To reproduce the issue, run the script with Python 3.9.6 or higher:
```
$ python3 reproducer.py
```
This should print a stack trace and exit with code 1, indicating that the issue is present.

The script sets up a dummy Sphinx project, then attempts to set up the `sphinx_gallery` extension with a version of `0.10.0`. This should not raise an exception, but due to the `needs_extensions` check using strings instead of versions, it does. The script catches this exception and prints a stack trace.

To fix the issue, the `needs_extensions` check should be updated to use version comparison instead of string comparison. For example, the following code snippet shows how the `needs_sphinx` attribute could be updated:
```python
# Before
self.needs_sphinx = '4.0.0'

# After
import sphinx
self.needs_sphinx = sphinx.__version__
```
This would ensure that version comparison is used instead of string comparison. Similar changes would need to be made to the `needs_gallery_version` attribute.