import datetime
from django.forms import Media

def create_media(MediaClass):
    return MediaClass(css={'all': ['main.css']}, js=['main.js'])

start = datetime.datetime.now()
media = create_media(Media)
for i in range(100000):
    media = media + create_media(Media)

try:
    # This should raise an AssertionError if the issue is present
    assert (datetime.datetime.now() - start).total_seconds() < 60, "Performance degraded"
except AssertionError as e:
    print_stacktrace(e)
    exit(1)  # Exit with code 1 when the issue is present

print('100000 additions took: %s' % (datetime.datetime.now() - start))
exit(0)  # Exit with code 0 when the issue is fixed
