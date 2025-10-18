# reproducer.py
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

try:
    # Simulated environment setup
    from argparse import ArgumentParser
    
    # Mocking Django's `add_arguments` and `call_command` functionalities
    parser = ArgumentParser(description="Mock parser to simulate Django command")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--foo', nargs='+', type=int)

    # Simulating `call_command('command_name', '--foo=1', '--foo=2', '--foo=3')`
    args = parser.parse_args(['--foo', '1', '--foo', '2', '--foo', '3'])
    assert args.foo == [1,2,3], "Issue found: nargs '+' not handled correctly within mutually exclusive group"

    # This point is reached only if no assertion error
    print("No issues detected.")

except Exception as e:
    print_stacktrace(e)
    sys.exit(1)  # Exiting with error code if any exception is raised

sys.exit(0)  # Exiting with success code if no issues
