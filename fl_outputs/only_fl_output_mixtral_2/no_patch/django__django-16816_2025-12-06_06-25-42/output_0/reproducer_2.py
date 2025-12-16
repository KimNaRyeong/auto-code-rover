import sys
import traceback

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def run_test():
    class Question:
        pass

    class Choice:
        pass

    class QuestionAdmin:
        list_display = ["choice"]

    try:
        QuestionAdmin.get_list_display(QuestionAdmin)[0]
    except Exception as e:
        assert False, f"Error E108 does not cover some cases: {e}"

if __name__ == "__main__":
    try:
        run_test()
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
