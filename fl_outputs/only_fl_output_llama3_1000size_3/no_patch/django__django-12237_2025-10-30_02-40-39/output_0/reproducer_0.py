import unicodedata
from django.utils.text import slugify

def main():
    title = "Hello İstanbul"
    slugified_title = slugify(title, allow_unicode=True)

    assert slugified_title.isalnum(), "Slug should be alphanumeric"

if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
    else:
        print("Issue not present")
        exit(0)
