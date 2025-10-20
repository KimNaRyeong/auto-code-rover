import re

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

def parse_enum_definition(code:str):
    """
    Simple parser to mimic the parsing of enum values including attributes.
    """
    parsed_values = []
    for line in code.split("\n"):
        match = re.match(r"^\s*(\w+)\s*(\w+)?\s*[,}]", line)
        if match:
            enum_value = match.group(1)
            parsed_values.append(enum_value)
    return parsed_values

def main():
    enum_declaration = """
typedef enum {
  JXL_TYPE_FLOAT = 0,
  JXL_TYPE_BOOLEAN JXL_DEPRECATED,
}
"""
    try:
        parsed_values = parse_enum_definition(enum_declaration)
        assert "JXL_TYPE_FLOAT" in parsed_values, "JXL_TYPE_FLOAT not found in parsed enum values"
        assert "JXL_TYPE_BOOLEAN" in parsed_values, "JXL_TYPE_BOOLEAN not found in parsed enum values"
        assert "JXL_DEPRECATED" not in parsed_values, "JXL_DEPRECATED was incorrectly identified as an enum value"
        print("Enum parsing validation passed!")
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    main()
