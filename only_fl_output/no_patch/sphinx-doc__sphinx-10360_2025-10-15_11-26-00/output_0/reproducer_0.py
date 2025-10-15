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

def parse_enum(enum_str):
    """
    Simplified enum parsing to simulate the reported issue.
    """
    lines = enum_str.strip().split("\n")
    enum_values = {}
    for line in lines:
        line = line.strip().rstrip(',')
        if line.startswith("/**") or line == "" or line.endswith("*/"):
            continue  # Skip documentation lines and empty lines
        elif "__deprecated__" in line:
            try:
                # Expected format: NAME ATTRIBUTE
                name, _ = line.split(" ")
                if name in enum_values:
                    raise ValueError(f"Duplicate enum value: {name}")
                enum_values[name] = "DEPRECATED"
            except ValueError as e:
                print_stacktrace(e)
                raise AssertionError("Failed to parse deprecated enum value correctly.") from e
        else:
            try:
                # Expected format: NAME = VALUE
                name, _ = line.split(" = ")
                enum_values[name] = "NORMAL"
            except ValueError as e:
                print_stacktrace(e)
                raise AssertionError("Failed to parse enum value correctly.") from e
    return enum_values

def test_enum_parsing():
    enum_example = """
    typedef enum {
    /** Use 32-bit single-precision floating point values, with range 0.0-1.0
    * (within gamut, may go outside this range for wide color gamut). Floating
    * point output, either JXL_TYPE_FLOAT or JXL_TYPE_FLOAT16, is recommended
    * for HDR and wide gamut images when color profile conversion is required. */
    JXL_TYPE_FLOAT = 0,
    
    /** DEPRECATED: Bitpacked 1-bit. As an alternative, use JXL_TYPE_UINT8.
    */
    JXL_TYPE_BOOLEAN JXL_DEPRECATED,
    
    } ExampleEnum;
    """
    
    enum_values = parse_enum(enum_example)
    assert "JXL_TYPE_FLOAT" in enum_values and enum_values["JXL_TYPE_FLOAT"] == "NORMAL", "JXL_TYPE_FLOAT not correctly parsed as NORMAL."
    assert "JXL_TYPE_BOOLEAN" in enum_values and enum_values["JXL_TYPE_BOOLEAN"] == "DEPRECATED", "JXL_TYPE_BOOLEAN not correctly parsed as DEPRECATED."
    print("Enum parsing test passed.")

if __name__ == "__main__":
    try:
        test_enum_parsing()
        print("No issues detected.")
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
    except Exception as unexpected_e:
        print(f"An unexpected error occurred: {unexpected_e}")
        exit(1)
