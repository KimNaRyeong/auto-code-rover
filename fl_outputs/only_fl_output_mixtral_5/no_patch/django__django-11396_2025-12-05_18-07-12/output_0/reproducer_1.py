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

class MyModel:
    pass

def reproduce_issue():
    try:
        cursor = MyModel.objects.raw("""
            CREATE TEMPORARY TABLE mymodel (
                id SERIAL PRIMARY KEY
            );
        """)
        cursor = MyModel.objects.raw("""
            INSERT INTO mymodel (id) VALUES (1), (2), (3);
        """)
        cursor = MyModel.objects.raw("""
            SELECT model.id FROM mymodel model ORDER BY 'asdf' ASC;
        """)
    except Exception as e:
        print_stacktrace(e)
        assert False

if __name__ == "__main__":
    reproduce_issue()
