import argparse
from datetime import datetime
import sys

def parse_duration_to_time(s):
    # dummy implementation, replace with actual parsing logic
    return datetime.now() + s

def parse_time(s):
    # dummy implementation, replace with actual parsing logic
    return datetime.strptime(s, "%Y-%m-%d %H:%M:%S")

class Command:
    def add_arguments(self, parser) -> None:
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument('--for', dest='until', action='store', type=parse_duration_to_time)
        group.add_argument('--until', dest='until', action='store', type=parse_time)

    def handle(self, until: datetime, **_) -> None:
        pass

def call_command(args):
    parser = argparse.ArgumentParser()
    command = Command()
    command.add_arguments(parser)
    namespace = parser.parse_args(args)
    command.handle(**vars(namespace))

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
        call_command(['--until', '2023-01-01 12:00:00'])
        assert False, "Expected error when calling command with --until"
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Failed to reproduce issue")

if __name__ == '__main__':
    main()
