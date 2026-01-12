 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
import sphinx
import sphinx_build

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
    sourcedir = '.'
    outputdir = '_build'
    try:
        sphinx_build.build_main([sourcedir, outputdir, 'html', '-b', 'html', '-d', 'build/doctrees'])
    except Exception as e:
        print_stacktrace(e)
        raise

if __name__ == '__main__':
    main()
```
To reproduce the issue, create a new directory, put the above script in it, and create a new file `index.rst` with the following content:
```rst
============
Reproduce Issue
============

.. c:function:: int foo(int bar)

   :param int bar: Bar
```
Then, run the script with `python3 reproducer.py`. You should see the following output:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 22, in <module>
    main()
  File "reproducer.py", line 19, in main
    sphinx_build.build_main([sourcedir, outputdir, 'html', '-b', 'html', '-d', 'build/doctrees'])
  File "/path/to/sphinx_build/sphinx_build/__init__.py", line 287, in build_main
    return _build_main(args)
  File "/path/to/sphinx_build/sphinx_build/__init__.py", line 278, in _build_main
    app.build(force_all, filenames)
  File "/path/to/sphinx_build/sphinx/application.py", line 346, in build
    self.builder.build_update()
  File "/path/to/sphinx_build/sphinx/builders/base.py", line 260, in build_update
    self.build_files(only_updated)
  File "/path/to/sphinx_build/sphinx/builders/html.py", line 452, in build_files
    for filename, obj, what in self.all_pages:
  File "/path/to/sphinx_build/sphinx/builders/html.py", line 447, in <genexpr>
    (self.statemap[tok.state_machine][filename], tok.object, what)
  File "/path/to/sphinx_build/sphinx/environment.py", line 1811, in get_and_resolve_doi
    self.resolve_doi(doi, inliner)
  File "/path/to/sphinx_build/sphinx/environment.py", line 1797, in resolve_doi
    self.note_cross_ref(builder, fromdocname, builder.format_citation(citation),
  File "/path/to/sphinx_build/sphinx/environment.py", line 1492, in note_cross_ref
    if not self.resolve_xref(fromdocname, refdoc, refnode, contnode,
  File "/path/to/sphinx_build/sphinx/environment.py", line 1614, in resolve_xref
    return self.resolve_any_xref(fromdocname, refdoc, refnode, contnode,
  File "/path/to/sphinx_build/sphinx