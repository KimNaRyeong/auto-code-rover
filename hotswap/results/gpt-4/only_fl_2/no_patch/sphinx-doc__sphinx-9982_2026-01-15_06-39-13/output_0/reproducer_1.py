import subprocess
import os
import re
import sys

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def get_project_root():
    script_dir = os.path.dirname(__file__)
    return os.path.join(script_dir)

def reproduce_issue():
    try:
        project_root = get_project_root()
        docs_dir = os.path.join(project_root, 'docs')
        if not os.path.exists(docs_dir):
            raise Exception(f"Expected docs directory at {docs_dir} does not exist")
        
        # Running the Sphinx build process
        result = subprocess.run(
            ["make", "html"],
            cwd=docs_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Mock patterns for different types of warnings to look for; these will need to be adjusted
        # based on the actual output and types of warnings expected to differ in color.
        warning_patterns = [
            r'WARNING: .*image file not readable',  # Example pattern for image warnings
            r'WARNING: .*unknown document',  # Example pattern for transition or other warnings
        ]

        found_warnings = {}

        # Check both stdout and stderr for warnings, could be configurable based on Sphinx config.
        for line in result.stdout.split("\n") + result.stderr.split("\n"):
            for pattern in warning_patterns:
                if re.search(pattern, line):
                    found_warnings[pattern] = found_warnings.get(pattern, 0) + 1

        if len(found_warnings) < len(warning_patterns):
            raise AssertionError("Not all types of warnings were detected")

        print("Different types of warnings detected successfully.")
        
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)  # Exit with an error code to indicate failure

if __name__ == "__main__":
    reproduce_issue()
