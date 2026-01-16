import logging
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

def test_foo():
    logging.getLogger().setLevel(42)

def test_bar():
    # Instead of using caplog, directly access the logger's level
    # This simulates reading the level in a subsequent test
    return logging.getLogger().level

def reset_logging_level():
    # Reset the log level to WARNING, the default level for logging
    logging.getLogger().setLevel(logging.WARNING)

try:
    test_foo()  # First test that sets the log level
    level_after_first_test = test_bar()  # Second test that checks the log level
    
    # Verify the log level was restored to WARNING or another expected level
    # since the issue is that the log level remains at 42 (the custom level set in test_foo)
    assert level_after_first_test == logging.WARNING, "Log level was not restored after test_foo."

except AssertionError as e:
    print_stacktrace(e)
    sys.exit(1)  # Exit with a non-zero code to indicate the presence of the issue

finally:
    # Ensure logging level is reset for any further operations
    reset_logging_level()
    
print("Issue not reproduced. Log level restored correctly.")
sys.exit(0)
