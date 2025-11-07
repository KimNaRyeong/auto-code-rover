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

def check_version_simulated_bug(required: str, current: str) -> bool:
    """Compares two version strings incorrectly, simulating the described bug."""
    # Simulate the string comparison bug
    return current > required

def main():
    try:
        # These values represent the scenario where the bug would be noticeable
        required_version = '0.6'
        current_version_should_pass = '0.10' # This is where we simulate the expected failure due to incorrect string comparison
        
        # Simulate the buggy behavior by using string comparison
        if not check_version_simulated_bug(required_version, current_version_should_pass):
            raise AssertionError(f"Current version {current_version_should_pass} should be considered newer than required version {required_version}")

        # If the code reaches here without an exception, it means the bug is not simulated correctly
        raise AssertionError("Simulated version comparison logic failed to reproduce the bug.")

    except AssertionError as e:
        print_stacktrace(e)
        exit(1) # Exit with code 1 if there's an AssertionError

if __name__ == "__main__":
    main()
