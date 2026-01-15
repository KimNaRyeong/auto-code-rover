# reproducer.py
import logging

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

class CapLogSimulator:
    def __init__(self):
        self.original_level = logging.getLogger().getEffectiveLevel()
        self.handler = logging.StreamHandler()
        logging.getLogger().addHandler(self.handler)

    def set_level(self, level):
        self.handler.setLevel(level)
        logging.getLogger().setLevel(level)

    def restore(self):
        logging.getLogger().setLevel(self.original_level)
        logging.getLogger().removeHandler(self.handler)

def test_foo(simulator):
    simulator.set_level(42)

def test_bar(simulator):
    if simulator.handler.level != 0:
        raise AssertionError(f"Expected log level 0, got {simulator.handler.level}")

def main():
    simulator = CapLogSimulator()
    try:
        test_foo(simulator)
        simulator.restore()  # Trying to mimic pytest's automatic restoration
        test_bar(simulator)
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
    else:
        print("Test passed: Log level was restored after the test.")
        exit(0)

if __name__ == "__main__":
    main()
