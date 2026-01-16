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

def test_seaborn_colorblind_style():
    import matplotlib.pyplot as plt
    try:
        the_rc = plt.style.library["seaborn-colorblind"]
        # If the key exists, then the test passes
        print("Test passed: 'seaborn-colorblind' style is accessible.")
    except KeyError as e:
        print_stacktrace(e)
        # The test should fail if a KeyError is raised
        raise AssertionError("KeyError raised for 'seaborn-colorblind' style")

if __name__ == "__main__":
    test_seaborn_colorblind_style()
