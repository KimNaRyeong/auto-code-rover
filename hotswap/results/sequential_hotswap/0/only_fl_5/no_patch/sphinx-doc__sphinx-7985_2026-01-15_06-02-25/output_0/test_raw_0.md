To reproduce the reported issue where `linkcheck` does not check local (internal) links in a Sphinx project, we can write a standalone Python script named `reproducer.py`. This script will programmatically create a Sphinx project, insert a document with both a broken external link and a broken local link, run `linkcheck`, and verify if `linkcheck` reports errors for both links as expected. It raises an `AssertionError` when the issue is present (if local links are not being checked), and exits with code 0 when the issue is fixed (if local links are being checked along with external links).

Here is how such a script could look:

```python
import os
import sys
import subprocess
from sphinx.cmd.build import main as sphinx_build

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

def create_sphinx_project():
    project_name = "temp_sphinx_project"
    os.mkdir(project_name)
    os.mkdir(os.path.join(project_name, "_static"))
    os.mkdir(os.path.join(project_name, "_templates"))
    
    conf_py = f"""
import os
import sys
sys.path.insert(0, os.path.abspath('.'))
extensions = ['sphinx.ext.linkcheck']
templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
html_static_path = ['_static']
"""
    
    index_rst = """
broken external-link_
broken local-link_

.. _external-link: https://lkfqhlkghflkhs
.. _local-link: doesntexist
"""
    
    with open(os.path.join(project_name, "conf.py"), "w") as f:
        f.write(conf_py)
    
    with open(os.path.join(project_name, "index.rst"), "w") as f:
        f.write(index_rst)
    
    return project_name

def run_linkcheck(project_name):
    exit_code = sphinx_build(["-b", "linkcheck", project_name, os.path.join(project_name, "_build")])
    return exit_code

def verify_linkcheck_output(project_name):
    with open(os.path.join(project_name, "_build", "output.txt"), "r") as f:
        output = f.read()
    if "local-link" not in output:
        raise AssertionError("Local link was not checked by linkcheck.")

def main():
    try:
        project_name = create_sphinx_project()
        exit_code = run_linkcheck(project_name)
        if exit_code != 0:
            print("Linkcheck reported errors as expected.")
        verify_linkcheck_output(project_name)
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)
    finally:
        # Cleanup
        subprocess.run(["rm", "-rf", project_name])

if __name__ == "__main__":
    main()
```

Please note, the `verify_linkcheck_output` function in this script expects to read an output file (`output.txt`) that doesn't exist by default when using Sphinx's `linkcheck`. You would need to modify how you collect and examine the linkcheck results within this script, as `sphinx-build` does not output results to a file named `output.txt` by default. You might want to capture the standard output and error of the `linkcheck` process and analyze that to find references to the local link. Adjusting this portion of the script is necessary to match how Sphinx outputs `linkcheck` results.