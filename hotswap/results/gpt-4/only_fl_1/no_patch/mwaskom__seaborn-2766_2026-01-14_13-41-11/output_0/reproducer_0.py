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

def check_seaborn_with_setuptools_warning():
    try:
        import sys
        import subprocess
        
        # Upgrade setuptools and install seaborn
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-U", "setuptools>=60"])
        subprocess.check_call([sys.executable, "-m", "pip", "install", "seaborn"])
        
        # Import seaborn with warnings treated as exceptions
        subprocess.check_output([sys.executable, "-We", "-c", "import seaborn"])
    except subprocess.CalledProcessError as e:
        raise AssertionError("The issue is present.") from e
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("An unexpected error occurred.") from e

if __name__ == "__main__":
    try:
        check_seaborn_with_setuptools_warning()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)  # Exiting with non-zero if assertion error (issue present)
    print("No DeprecationWarning detected. The issue is fixed.")
    exit(0)
