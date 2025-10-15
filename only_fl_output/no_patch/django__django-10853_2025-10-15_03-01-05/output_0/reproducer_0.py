import sqlite3
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

def main():
    try:
        conn = sqlite3.connect(":memory:")
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE t0(x INTEGER PRIMARY KEY, y TEXT)")
        cursor.execute("INSERT INTO t0 VALUES (1, 'aaa'), (2, 'ccc'), (3, 'bbb')")
        cursor.execute("SELECT x, y, row_number() OVER (ORDER BY y) AS row_number FROM t0 ORDER BY x")
        # If the exception is not raised, assert fails and indicates the issue is fixed
        assert False, "SQLite now supports window functions. The issue is fixed."
    except sqlite3.OperationalError as e:
        print_stacktrace(e)
        assert e.args[0].startswith('near "(": syntax error'), "Unexpected OperationalError: " + e.args[0]
    
    except AssertionError as e:
        print_stacktrace(e)
        raise e

    except Exception as e:
        print_stacktrace(e)
        assert False, f"Unexpected error: {e}"

if __name__ == "__main__":
    main()
    sys.exit(0)
