import argparse
from datetime import datetime
import sys

def parse_duration_to_time(value):
    # dummy implementation, replace with actual parsing logic
    return value

def parse_time(value):
    # dummy implementation, replace with actual parsing logic
    return value

class Command:
    def add_arguments(self, parser) -> None:
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument('--for', dest='until', action='store', type=parse_duration_to_time)
        group.add_argument('--until', dest='until', action='store', type=parse_time)

    def handle(self, until: str, **_) -> None:
        pass

def call_command(command, *args, **kwargs):
    parser = argparse.ArgumentParser()
    command.add_arguments(parser)
    namespace = parser.parse_args(args)
    return command.handle(**vars(namespace))

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
    command = Command()
    
    # This should fail due to the issue
    try:
        call_command(command, '--until', '2022-01-01')
    except Exception as e:
        pass  # this should not raise an exception
    
    # This should also fail due to the issue
    try:
        call_command(command, '--for', '1 hour')
    except TypeError as e:
        print_stacktrace(e)
        assert True, "Expected failure when calling command with --for value"
    else:
        assert False, "Did not fail when calling command with --for value"

if __name__ == "__main__":
    main()
