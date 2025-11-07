import argparse
from datetime import datetime
import sys

def parse_duration_to_time(s):
    # dummy implementation, replace with actual parsing logic
    return s  # return the input string for simplicity

def parse_time(s):
    # dummy implementation, replace with actual parsing logic
    return s  # return the input string for simplicity

class Command:
    def add_arguments(self, parser) -> None:
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument('--for', dest='until', action='store', type=parse_duration_to_time)
        group.add_argument('--until', action='store', type=parse_time)

def call_command(args):
    parser = argparse.ArgumentParser()
    command = Command()
    command.add_arguments(parser)
    namespace = parser.parse_args(args)
    return namespace

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
        # Try to call the command with --until argument
        namespace = call_command(['--until', '2023-03-01T12:00:00'])
        assert hasattr(namespace, 'until'), "Expected 'until' attribute"

        # Try to call the command with --for argument (this should fail)
        try:
            namespace = call_command(['--for', '1 hour'])
            assert False, "Expected error when passing --for argument"
        except Exception as e:
            print_stacktrace(e)
            raise AssertionError("Failed to pass --for argument")

    except AssertionError as e:
        print(f"AssertionError: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
