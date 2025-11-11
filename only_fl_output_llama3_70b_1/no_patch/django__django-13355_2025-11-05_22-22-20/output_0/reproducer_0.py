from django.forms import Media
import datetime
import time

def create_media(MediaClass):
    return MediaClass(css={'all': ['main.css']}, js=['main.js'])

start = datetime.datetime.now()
media = create_media(Media)
for i in range(100000):
    media = media + create_media(Media)

end = datetime.datetime.now()
duration = (end - start).total_seconds()

if duration > 60:  # if it takes more than 1 minute
    raise AssertionError("Media.__add__ performance issue detected")

print(f"100000 additions took: {duration:.2f} seconds")
