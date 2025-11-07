def check_version(min_required: str, installed: str) -> bool:
    """Compares version strings to determine if the installed version meets the minimum requirement."""
    return installed >= min_required

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

def main():
    min_version_required = '0.6'
    installed_version = '0.10'
    try:
        assert check_version(min_version_required, installed_version), (
            f"Version {installed_version} should be considered newer than {min_version_required}"
        )
    except AssertionError as e:
        print_stacktrace(e)
        raise SystemExit(1)

    print("Version check passed. The issue is fixed.")

if __name__ == "__main__":
    main()
