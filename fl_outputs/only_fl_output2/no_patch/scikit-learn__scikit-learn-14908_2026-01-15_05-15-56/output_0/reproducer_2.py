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

def test_error_message_improvement():
    try:
        from sklearn.dummy import DummyClassifier
        clf = DummyClassifier(strategy='constant', constant='not-in-dataset')
        clf.fit([[1., 2.]], ['class1'])
    except ValueError as e:
        expected_message_part = "The constant target value must be present in the training data"
        if expected_message_part in str(e):
            print("The original error message is present. Checking for improvement...")
            provided_value = "constant='not-in-dataset'"
            possible_values = "Possible values are: ['class1']"
            if provided_value in str(e) and possible_values in str(e):
                print("Error message has been improved to be more informative")
                exit(0)
            else:
                print_stacktrace(e)
                raise AssertionError("The error message does not include the improvement.")
        else:
            print_stacktrace(e)
            raise AssertionError("The expected part of the original error message is not present.")
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("An unexpected error occurred.")
    else:
        raise AssertionError("Expected ValueError not raised, indicating the issue might have been fixed without the expected error message.")

if __name__ == "__main__":
    test_error_message_improvement()
