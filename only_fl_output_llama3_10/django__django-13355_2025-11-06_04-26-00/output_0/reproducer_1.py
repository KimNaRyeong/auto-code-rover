import datetime
from django.forms import Media

def create_media(MediaClass):
    return MediaClass(css={'all': ['main.css']}, js=['main.js'])

start = datetime.datetime.now()
media = create_media(Media)
for i in range(100000):
    media = media + create_media(Media)

try:
    assert (datetime.datetime.now() - start).total_seconds() < 60, "Performance issue detected"
except AssertionError as e:
    print_stacktrace(e)
    raise
