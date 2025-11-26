import json
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

def test_unicode_chars_in_jsonfield():
    chinese_chars = '中国'
    data = {'json_field': chinese_chars}
    json_data = json.dumps(data, ensure_ascii=True)
    try:
        assert chinese_chars in json_data
        print("Issue is fixed!")
        sys.exit(0)
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == '__main__':
    test_unicode_chars_in_jsonfield()
