import json

def test_unicode_chars_in_json():
    chinese_str = '中国'
    try:
        json_str = json.dumps(chinese_str)
        assert json_str == '"中国"', "Unicode chars not displayed properly in JSON"
    except AssertionError as e:
        print_stacktrace(e)
        raise

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

if __name__ == '__main__':
    test_unicode_chars_in_json()
