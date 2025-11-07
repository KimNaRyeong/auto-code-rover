import subprocess
import os
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
    
def run_pytest_with_logfile_option():
    log_file_path = "subtest/test.log"
    try:
        # Assuming pytest is installed in the environment
        command = f"pytest --log-file={log_file_path}"
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        if "no such file or directory" in result.stderr.lower():
            raise FileNotFoundError("Pytest failed to create subdirectories for the log file.")
        print("Pytest executed successfully. The issue is likely fixed.")
        sys.exit(0)
    except subprocess.CalledProcessError as e:
        print_stacktrace(e)
        raise AssertionError("Pytest execution failed, reproducing the reported issue.")
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("An unexpected error occurred.")

if __name__ == "__main__":
    run_pytest_with_logfile_option()
