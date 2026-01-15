import matplotlib as mpl
from matplotlib import rcParamsDefault
from pathlib import Path
import tempfile
from unittest import mock
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

def test_issue_1713_reproducer():
    # Creating a temporary directory
    with tempfile.TemporaryDirectory() as tmpdirname:
        rcpath = Path(tmpdirname) / 'test_rcparams.rc'
        rcpath.write_text('timezone: UTC', encoding='utf-32-be')
        
        # Mocking the locale to use UTF-32-BE encoding
        with mock.patch('locale.getpreferredencoding', return_value='utf-32-be'):
            try:
                # This line should fail if the issue exists
                rc = mpl.rc_params_from_file(rcpath, True, False)
                assert rc.get('timezone') == 'UTC', "The timezone setting was not correctly read from the rc file."
            except UnicodeDecodeError as e:
                print_stacktrace(e)
                sys.exit(1)
    # If no exception is raised, the script exits with code 0, indicating the issue is fixed.
    print("Success: No issue detected.")
    
if __name__ == "__main__":
    try:
        with mock.patch("locale.getpreferredencoding", return_value="utf-32-be"):
            # Attempting to import matplotlib with a mocked encoding that would raise an exception if the issue exists
            import matplotlib
        rcParamsDefault  # Attempt to access a potentially uninitialized variable if matplotlib failed to import properly
    except Exception as e:  # Catching any exception that indicates failure to properly handle file encodings
        print_stacktrace(e)
        sys.exit(1)
    else:
        # If matplotlib imports successfully under mocked utf-32-be encoding, proceed to run the test
        test_issue_1713_reproducer()
