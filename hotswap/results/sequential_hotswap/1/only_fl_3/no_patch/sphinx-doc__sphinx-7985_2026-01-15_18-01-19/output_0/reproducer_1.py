import os
import subprocess
import sys

def print_stacktrace(e: Exception):
    import traceback
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def setup_sphinx_project():
    project_dir = 'test_sphinx_project'
    os.makedirs(project_dir, exist_ok=True)
    conf_py = os.path.join(project_dir, 'conf.py')
    index_rst = os.path.join(project_dir, 'index.rst')

    # Minimal Sphinx config
    with open(conf_py, 'w') as f:
        f.write("extensions = ['sphinx.ext.intersphinx']")
        f.write("\nsource_suffix = '.rst'")
        f.write("\nmaster_doc = 'index'")
        f.write("\nhtml_theme = 'alabaster'\n")

    # index.rst with both broken external and local links as described
    with open(index_rst, 'w') as f:
        f.write('.. _external-link: https://lkfqhlkghflkhs\n')
        f.write('.. _local-link: doesntexist\n\n')
        f.write('broken external-link_\n')
        f.write('broken local-link_\n')

    return project_dir

def run_linkcheck(project_dir):
    cmd = ['sphinx-build', '-b', 'linkcheck', project_dir, os.path.join(project_dir, '_build')]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result

def validate_linkcheck_output(output):
    link_errors = ['broken external-link_', 'broken local-link_']
    for error in link_errors:
        if error not in output:
            raise AssertionError(f"Expected to find link check error for: {error}")

if __name__ == "__main__":
    try:
        project_dir = setup_sphinx_project()
        result = run_linkcheck(project_dir)
        
        # Validate the output to ensure both links are checked
        validate_linkcheck_output(result.stdout)

        print("Test passed: Both external and local links are being checked.")
    except AssertionError as ae:
        print_stacktrace(ae)
        sys.exit(1)
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)
    else:
        sys.exit(0)
