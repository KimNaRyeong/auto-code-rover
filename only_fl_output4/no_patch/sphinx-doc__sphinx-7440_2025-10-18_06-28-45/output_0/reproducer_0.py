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

def check_glossary_for_duplicates(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        terms = set()
        for line in lines:
            if line.startswith('.. glossary::'):
                continue  # Skip the directive line
            trimmed_line = line.strip().lower()  # Normalize case
            # Check for terms, which are indented
            if trimmed_line and line.startswith(' '):
                term = trimmed_line.split()[0]  # Get the first word
                if term in terms:
                    raise ValueError(f"Duplicate term detected: {term}")
                terms.add(term)

def main():
    try:
        check_glossary_for_duplicates('doc/glossary.rst')
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Duplicate term issue detected.") from e
    else:
        print("No duplicate terms detected. Issue is fixed.")
        exit(0)

if __name__ == "__main__":
    main()
