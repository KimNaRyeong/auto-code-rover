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

def main():
    try:
        import matplotlib.pyplot as plt
        plt.subplots(1, 1, figsize=(3, 0))
        plt.savefig("test.png")
    except RuntimeError as e:
        if "libpng" in str(e):
            print_stacktrace(e)
            raise AssertionError("Issue reproduced: 'libpng signaled error'") from e
        else:
            print_stacktrace(e)
            raise AssertionError("Unexpected RuntimeError, not a libpng error.") from e
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("An unexpected exception occurred.") from e
    else:
        print("The issue seems to be resolved, exiting with code 0.")
        exit(0)

if __name__ == "__main__":
    main()
