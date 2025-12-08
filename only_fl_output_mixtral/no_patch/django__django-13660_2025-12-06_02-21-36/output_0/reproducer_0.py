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

def handle(options):
    # Execute the command and exit.
    if options['command']:
        exec(options['command'])
        return

if __name__ == "__main__":
    try:
        # Simulate the issue by passing the -c option with a string containing a function definition
        handle({'command': "import django\ndef f():\n\tprint(django.__version__)\nf()"})
    except Exception as e:
        print_stacktrace(e)
        assert False, "Issue reproduced"
