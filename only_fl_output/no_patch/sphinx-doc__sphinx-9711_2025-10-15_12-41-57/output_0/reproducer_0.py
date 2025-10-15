def check_version(current_version: str, minimum_version: str) -> bool:
    """Checks if the current version is not less than the minimum required version."""
    return current_version >= minimum_version

def simulate_extension_version_check():
    minimum_required_version = "0.6"
    installed_version = "0.10"
    
    # This is where the issue is simulated: comparing versions as strings can lead to incorrect results.
    if check_version(installed_version, minimum_required_version):
        return True
    else:
        raise AssertionError("Installed version is incorrectly considered not new enough.")

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
    try:
        assert simulate_extension_version_check(), "Version comparison logic is flawed."
    except AssertionError as e:
        print_stacktrace(e)
        raise e
    print("Version comparison logic is correct.")
