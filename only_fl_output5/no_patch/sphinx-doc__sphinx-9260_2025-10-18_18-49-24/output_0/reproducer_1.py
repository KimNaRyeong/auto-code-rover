import urllib.request
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

def fetch_page_source(url: str) -> str:
    try:
        with urllib.request.urlopen(url) as response:
            return response.read().decode('utf-8')
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

def check_anchor_in_source(source_code: str, anchor: str) -> bool:
    return f'id="{anchor}"' in source_code or f'name="{anchor}"' in source_code

def main():
    base_url = "https://github.com/crate/crate-docs-theme/blob/master/DEVELOP.rst"
    original_anchor = "make-changes"
    new_anchor = "user-content-make-changes"
    
    page_source = fetch_page_source(base_url)
    
    original_exists = check_anchor_in_source(page_source, original_anchor)
    new_exists = check_anchor_in_source(page_source, new_anchor)
    
    # Expecting the new anchor style to work, given the described issue.
    try:
        assert new_exists, f"New style anchor '{new_anchor}' not found in source."
        assert original_exists, f"Original style anchor '{original_anchor}' should also exist."
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
    
    print("Both original and new style anchors exist in source. Issue not reproduced.")
    sys.exit(0)

if __name__ == "__main__":
    main()
