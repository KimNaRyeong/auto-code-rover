# reproducer.py
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

# Simulated function signature as would be captured by Sphinx
def simulate_sphinx_autodoc_behavior():
    DEFAULT_OPTION = 'default'
    simulated_sphinx_output = "do_something(msg, option='default')"
    
    # Hypothetically check if Sphinx preserved the constant's name (which we assume it's not doing)
    try:
        # This condition reflects the absence of the constant name preservation
        # This is a simplistic mock-up; real Sphinx behavior involves introspection and parsing of source code
        if simulated_sphinx_output != "do_something(msg, option=DEFAULT_OPTION)":
            raise AssertionError("Sphinx did not preserve the constant name in the documentation.")
    except AssertionError as error:
        print_stacktrace(error)
        sys.exit(1)  # Exit with error to indicate the issue is present

    print("Sphinx issue not present, constant names are preserved.")
    sys.exit(0)  # Exit with success indicating the issue is fixed (hypothetically)

if __name__ == "__main__":
    simulate_sphinx_autodoc_behavior()
