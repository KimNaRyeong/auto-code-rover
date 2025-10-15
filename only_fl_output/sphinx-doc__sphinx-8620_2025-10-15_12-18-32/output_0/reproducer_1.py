# reproducer.py
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
    try:
        # Mocked HTML output based on the issue description. In a real scenario, this would
        # come from parsing RST through Sphinx and examining the resultant HTML file.
        generated_html_single = '<kbd class="kbd docutils literal notranslate">A</kbd>'
        generated_html_compound = (
            '<kbd class="kbd docutils literal notranslate">'
            '<kbd class="kbd docutils literal notranslate">Shift</kbd>+'
            '<kbd class="kbd docutils literal notranslate">X</kbd>'
            '</kbd>'
        )

        # Expected HTML outcome after the hypothetical issue fix.
        # In reality, this requires confirmation by examining the Sphinx output.
        expected_html_compound_fixed = (
            '<kbd class="kbd compound docutils literal notranslate">'
            '<kbd class="kbd docutils literal notranslate">Shift</kbd>+'
            '<kbd class="kbd docutils literal notranslate">X</kbd>'
            '</kbd>'
        )

        # Asserting generated against expected HTML to simulate replicating and detecting the issue.
        assert generated_html_single.find('<kbd class="kbd docutils literal notranslate">A</kbd>') != -1, "Single keystroke HTML not as expected"
        assert generated_html_compound.find('<kbd class="kbd compound docutils literal notranslate">') == -1, "Issue is present; compound keystroke HTML not as expected"
        
        if expected_html_compound_fixed in generated_html_compound:
            print("Issue is possibly fixed, compound keystroke HTML includes distinct class.")
        else:
            raise AssertionError("Issue not fixed; compound keystroke HTML does not include distinct class.")

    except Exception as e:
        print_stacktrace(e)
        exit(1)


if __name__ == "__main__":
    main()
