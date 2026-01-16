import os
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

# Mocking the structure of a .pot file with duplicates
pot_data = """
#: ../../manual/modeling/hair.rst:0
#: ../../manual/modeling/hair.rst:0
msgid "Type"
msgstr ""
"""

def uniqueLocation(locations):
    loc_set = set(locations)
    return list(loc_set)

def check_duplicates(content):
    lines = content.split("\n")
    locations = []
    for line in lines:
        if line.startswith("#:"):
            location = line[2:].strip()
            locations.append(location)
    if len(locations) != len(uniqueLocation(locations)):
        raise AssertionError("Duplicate locations found")
    return "No duplicates were found. All good!"

def main():
    try:
        result = check_duplicates(pot_data)
        print(result)
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)  # Exit with an error code when an AssertionError is caught

if __name__ == "__main__":
    main()
