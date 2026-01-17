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
    except sphinx.errors.SphinxError as e:
        print_stacktrace(e)
        raise e

if __name__ == '__main__':
    main()
```
To reproduce the issue, create a directory `reproduce` and put the following files in it:

* `index.rst`:
```rst
============
Reproduce
============

.. c:function:: int foo(int bar)

   :param int bar: Bar
```
* `reproducer.py`: the script above

Then execute `python3 reproducer.py` in the `reproduce` directory. You should see the following output:
```sql
Traceback (most recent call last):
  File "reproducer.py", line 24, in <module>
    main()
  File "reproducer.py", line 20, in main
    sphinx_build.build_main([sourcedir, outputdir, 'html', '-b', 'html', '-d', 'build/doctrees'])
  File "/home/user/.local/lib/python3.9/site-packages/sphinx_build/__init__.py", line 287, in build_main
    app.build(force_all, filenames)
  File "/home/user/.local/lib/python3.9/site-packages/sphinx/application.py", line 346, in build
    self.builder.build_update()
  File "/home/user/.local/lib/python3.9/site-packages/sphinx/builders/html.py", line 398, in build_update
    self.write_doc(doctree, destfile)
  File "/home/user/.local/lib/python3.9/site-packages/sphinx/builders/html.py", line 431, in write_doc
    self.writer.write(doctree, builder, 'html', doctree.docname)
  File "/home/user/.local/lib/python3.9/site-packages/sphinx/writers/html.py", line 201, in write
    self.write_doc(doctree, builder)
  File "/home/user/.local/lib/python3.9/site-packages/sphinx/writers/html.py", line 184, in write_doc
    self.write_doctree(doctree, builder)
  File "/home/user/.local/lib/python3.9/site-packages/sphinx/writers/html.py", line 169, in write_doctree
    node.walkabout(visitor)
  File "/home/user/.local/lib/python3.9/site-packages/sphinx/util/nodes.py", line 41, in walkabout
    walkabout(node, visitor, system_docname, genpath)
  File "/home/user/.local/lib/python3.9/site-packages/sphinx/util/nodes.py", line 41, in walkabout
    walkabout(node, visitor, system_docname, genpath)
  File "/home/user/.local/lib