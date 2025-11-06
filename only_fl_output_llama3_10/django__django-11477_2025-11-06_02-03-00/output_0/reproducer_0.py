import re
from urllib.parse import urlparse, urlunparse

def translate_url(pattern):
    return pattern.format(**{'group1': 'value1', 'group2': ''})

def main():
    pattern = r'(?P<group1>.*?)/(?P<group2>.*?)/'
    try:
        translated_url = translate_url(pattern)
        assert urlparse(translated_url).path == '/value1//', "URL translation failed"
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    main()
