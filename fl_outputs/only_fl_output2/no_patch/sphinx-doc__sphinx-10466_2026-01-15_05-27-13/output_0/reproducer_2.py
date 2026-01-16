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

class MockMessage:
    def __init__(self, text: str, locations):
        self.text = text
        self.locations = locations

    def unique_locations(self):
        unique_loc = list(set(self.locations))
        if len(unique_loc) != len(self.locations):
            raise AssertionError("Duplicated locations found!")
        return unique_loc

def reproduce_issue():
    # Simulating a scenario where locations are duplicated due to a bug
    duplicate_locations = [
        ("../../manual/modeling/hair.rst", 0),
        ("../../manual/modeling/hair.rst", 0),  # Duplicate
        ("../../manual/render/shader_nodes/vector/vector_rotate.rst", 38),
    ]
    
    message = MockMessage("Type", duplicate_locations)
    try:
        message.unique_locations()
    except AssertionError as e:
        print_stacktrace(e)
        return False  # Issue reproduced
    return True  # Issue not reproduced

def main():
    if not reproduce_issue():
        print("The issue was successfully reproduced.")
        exit(1)  # Exiting with code 1 to indicate the presence of an issue
    else:
        print("No issue detected.")
        exit(0)  # Exiting with code 0 indicating no issue or it's fixed

if __name__ == "__main__":
    main()
