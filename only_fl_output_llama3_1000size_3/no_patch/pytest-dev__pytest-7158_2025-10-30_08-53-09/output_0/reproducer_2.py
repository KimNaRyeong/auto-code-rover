import os
import sys
from pathlib import Path

def test_issue():
    current_dir = str(Path(__file__).parent.absolute())
    tested_file_path = f"{current_dir}/my_tests/test1.py"
    invocation_dir = os.getcwd()

    if not os.path.exists(tested_file_path):
        pytest.skip("Test file does not exist")
    else:
        try:
            import subprocess
            result = subprocess.run(['pytest', '-rs', '../my_tests/test1.py'], cwd=current_dir, capture_output=True, text=True)
            if result.returncode != 0:
                print_stacktrace(subprocess.CalledProcessError(result.returncode, 'pytest'))
                raise AssertionError("Issue not reproduced")
        except subprocess.CalledProcessError as e:
            print_stacktrace(e)

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

if __name__ == "__main__":
    test_issue()
