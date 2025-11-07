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

def create_sphinx_project():
    subprocess.check_call([sys.executable, '-m', 'sphinx.cmd.quickstart', '--quiet', '--sep', '-p', 'TestProject', '-a', 'Author', 'docs'])
    with open('docs/conf.py', 'a') as conf:
        conf.write("\nextensions = ['sphinx.ext.inheritance_diagram']\n")
    os.makedirs('docs/my_package', exist_ok=True)
    with open('docs/my_package/my_class_1.rst', 'w') as f:
        f.write(".. inheritance-diagram:: MyPackage.MyClass1\n")
    with open('docs/index.rst', 'w') as f:
        f.write("Welcome to TestProject's documentation!\n==================================\n\n.. toctree::\n\n   my_package/my_class_1\n")

def check_svg_links():
    svg_file_path = 'docs/_build/html/my_package/my_class_1.html'
    expected_substring = 'my_package/my_class_1.html#mypackage.myclass1'

    try:
        with open(svg_file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            assert expected_substring in content, "SVG link does not point correctly."
    except FileNotFoundError:
        raise FileNotFoundError(f"Expected file was not generated: {svg_file_path}")

try:
    create_sphinx_project()
    # Generate documentation
    subprocess.check_call(['sphinx-build', '-b', 'html', 'docs', 'docs/_build/html'])

    # Check if SVG links are correct
    check_svg_links()

    print("Success: No issue found with SVG links; they point correctly.")

except Exception as e:
    print_stacktrace(e)
    sys.exit(1)
