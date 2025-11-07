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

def simulate_sphinx_processing():
    """
    Mock function that simulates the Sphinx HTML processing of the :kbd: role,
    mimicking the described behavior in the issue.
    """
    single_key_output = '<kbd class="kbd docutils literal notranslate">A</kbd>'
    compound_key_output = """
<kbd class="kbd docutils literal notranslate">
  <kbd class="kbd docutils literal notranslate">Shift</kbd>+
  <kbd class="kbd docutils literal notranslate">X</kbd>
</kbd>
"""
    return single_key_output, compound_key_output

def check_for_issue():
    single_key, compound_key = simulate_sphinx_processing()

    # Check if compound_key has only the same classes as single_key elements without an added class to distinguish them
    if 'compound' not in compound_key:
        raise AssertionError("Compound `kbd` elements are not differentiated from single `kbd` elements by a specific class.")

def main():
    try:
        check_for_issue()
        # If no exception is raised, exit with code 0 indicating the issue is fixed
        print("Issue seems to be fixed, exiting with code 0.")
        exit(0)
    except AssertionError as e:
        print_stacktrace(e)
        # Exit with a non-zero exit code to indicate the presence of the issue
        exit(1)

if __name__ == "__main__":
    main()
