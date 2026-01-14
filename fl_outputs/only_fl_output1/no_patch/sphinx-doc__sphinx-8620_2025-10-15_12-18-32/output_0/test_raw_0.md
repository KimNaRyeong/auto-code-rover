```python
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

def main():
    from sphinx.application import Sphinx
    import os

    # Create a minimal Sphinx project
    try:
        os.makedirs('test_project/source', exist_ok=True)
        with open('test_project/source/conf.py', 'w') as f:
            f.write("extensions = []")

        with open('test_project/source/index.rst', 'w') as f:
            f.write(":kbd:`A`\n\n:kbd:`Shift+X`")

        app = Sphinx(
            srcdir='test_project/source',
            confdir='test_project/source',
            outdir='test_project/build',
            doctreedir='test_project/doctree',
            buildername='html'
        )
        app.build()

        # Read the generated HTML
        with open('test_project/build/index.html', 'r') as f:
            html_content = f.read()

        # Check if the generated HTML matches the expected output
        expected_single = '<kbd class="kbd docutils literal notranslate">A</kbd>'
        expected_compound = (
            '<kbd class="kbd compound docutils literal notranslate">'
            '<kbd class="kbd docutils literal notranslate">Shift</kbd>+'
            '<kbd class="kbd docutils literal notranslate">X</kbd>'
            '</kbd>'
        )

        assert expected_single in html_content, "Single keystroke HTML not as expected"
        if expected_compound not in html_content:
            raise AssertionError("Compound keystroke HTML not as expected")
        
        print("Issue is not present, generated HTML is as expected.")

    except Exception as e:
        print_stacktrace(e)
        exit(1)


if __name__ == "__main__":
    main()
```