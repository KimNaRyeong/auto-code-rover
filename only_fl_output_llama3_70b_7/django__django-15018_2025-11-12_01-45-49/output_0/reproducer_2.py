import argparse
from datetime import datetime
import sys

def parse_duration_to_time(value):
    # dummy implementation, replace with actual parsing logic
    return value  # return the original value for simplicity

def parse_time(value):
    # dummy implementation, replace with actual parsing logic
    return value  # return the original value for simplicity

class Command:
    def add_arguments(self, parser) -> None:
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument('--for', dest='until', action='store', type=parse_duration_to_time)
        group.add_argument('--until', dest='until', action='store', type=parse_time)

    def handle(self, until: str, **_) -> None:
        pass

def call_command(command, **kwargs):
    parser = argparse.ArgumentParser()
    command.add_arguments(parser)
    namespace = argparse.Namespace(**kwargs)
    try:
        command.handle(**vars(namespace))
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Failed to call command")

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
    
    try:
        call_command(command, until='2023-01-01 12:00:00')
    except AssertionError as e:
        print_stacktrace(e)
        raise
    
    try:
        call_command(command, for_='1 hour')  # this should fail because 'for' is not a valid keyword argument
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == '__main__':
    main()
