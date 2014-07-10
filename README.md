MJPEG TOOLS
===========

I use this to get live camera feed.
You can manipulate the image on the fly with PIL.

everything is processed in memory so it need to be fast.

### Requirments :
- Python >= 2.7
- PIL

### Usage :
copy server.py into your project(it is still not a package [no Time!])

to grab a single frame from mjpeg and save it to disk :
```
from server import MjpegParser
image = MjpegParser(url='http://path-to-your-camera-mjpeg').serve()
with open('imagename.jpg', 'wb') as im:
  im.write(image.read())
```

to simply grab infinite frames from mjpeg and save it to disk  I would do:
```
from server import MjpegParser
from time import time
While True:
  filename = str(time()).replace('.','') + '.' + 'jpeg'
  image = MjpegParser(url='http://path-to-your-camera-mjpeg').serve()
  with open(filename, 'wb') as im:
    im.write(image.read())
```

### Website
Use generator.
if you are using Django you can use *HttpResponse*
for flask you can use *Response*
