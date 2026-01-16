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

def uniq(iterable):
    seen = set()
    for element in iterable:
        if element not in seen:
            yield element
            seen.add(element)

def test_uniq_with_list_modification():
    f = list('THISTLE')
    try:
        for i in uniq(f):
            f.remove(i)
        raise AssertionError("List was modified during iteration without error.")
    except RuntimeError as e:
        print("Caught expected RuntimeError due to modification during iteration:", e)
    except Exception as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    try:
        test_uniq_with_list_modification()
        print("No RuntimeError caught. Issue likely not fixed.")
        exit(1)  # Expecting to catch RuntimeError, so if not, the issue still exists.
    except AssertionError as error:
        print_stacktrace(error)
        # If AssertionError is raised, it indicates the anticipated error mechanism didn't trigger,
        # suggesting an issue with list modification safety.
