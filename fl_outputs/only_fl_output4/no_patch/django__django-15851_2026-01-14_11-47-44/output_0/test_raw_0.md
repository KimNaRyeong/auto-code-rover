```python
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

def run_dbshell(database_name, extra_args):
    cmd = ['psql', database_name] + extra_args
    result = subprocess.run(cmd, text=True, capture_output=True)
    return result

def reproduce_issue():
    database_name = "some_database" # Replace with your actual database name
    extra_args = ["-c", "select * from some_table;"]
    result = run_dbshell(database_name, extra_args)
    if "extra command-line argument" in result.stderr:
        return True
    return False

def main():
    try:
        issue_present = reproduce_issue()
        assert not issue_present, "Issue reproduced: dbshell extra parameters not correctly parsed before dbname."
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1) # Exit the script with an error code

    print("No issue detected.")
    sys.exit(0) # Exit the script successfully

if __name__ == "__main__":
    main()
```

This script aims to reproduce the problem where passing extra parameters to `psql` through a wrapper improperly places those parameters after the database name, causing `psql` to ignore them. If the script identifies the issue (based on the presence of warning messages in the `stderr` output from `psql`), it raises an `AssertionError`, prints a detailed stack trace of the script up to the assertion, and exits with code 1, indicating an error. If no issue is detected, it simply prints a success message and exits with code 0. 

Note: Ensure you have `psql` installed and correctly configured to use this script, and replace `"some_database"` with an actual database name that exists in your PostgreSQL setup.