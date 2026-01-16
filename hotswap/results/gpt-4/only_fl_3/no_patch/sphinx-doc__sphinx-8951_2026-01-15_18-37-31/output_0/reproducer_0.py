import subprocess
import os
import shutil
from typing import Any

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

def setup_sphinx_project():
    # Create a minimal Sphinx project
    project_name = "test_sphinx"
    srcdir = f"./{project_name}"
    conf_py = os.path.join(srcdir, "conf.py")
    index_rst = os.path.join(srcdir, "index.rst")
    os.makedirs(srcdir, exist_ok=True)

    with open(conf_py, "w") as f:
        f.write("project = 'TestProject'\n")
        f.write("extensions = ['breathe']\n")
        f.write("breathe_projects = { 'test': './xml' }\n")
        f.write("breathe_default_project = 'test'\n")
        f.write("highlight_language = 'c++'\n")

    with open(index_rst, "w") as f:
        f.write(".. cpp:function:: std::strong_ordering operator<=>(Foo, Foo)\n")

def run_sphinx():
    # Build the Sphinx documentation
    result = subprocess.run(["sphinx-build", "-b", "html", "./test_sphinx", "./test_sphinx/_build"], capture_output=True, text=True)
    return result.stderr
    
def reproduce_issue():
    setup_sphinx_project()
    try:
        build_output = run_sphinx()
        assert "WARNING: Error when parsing function declaration." not in build_output, "Issue with parsing spaceship operator found."
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Failed to verify the documentation. See stacktrace above.") from e

if __name__ == "__main__":
    try:
        reproduce_issue()
    except AssertionError as e:
        print("Issue reproduced successfully.")
        raise e
    else:
        print("No issue found. The spaceship operator seems to be supported.")
