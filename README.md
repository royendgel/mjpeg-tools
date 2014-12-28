[![Build Status](https://travis-ci.org/royendgel/mjpeg-tools.svg?branch=master)](https://travis-ci.org/royendgel/mjpeg-tools)

MJPEG TOOLS
===========

I use this to get live camera feed.
You can manipulate the image on the fly with PIL.

everything is processed in memory so it is suposed to be fast.

### Requirements :
- Python >= 2.7
- PIL

### Installation :
#### using pip(recommended) :
`pip install mjpeg-tools`

#### manual :
clone this project and run `sudo python setup.py install`

#### manual (not recommended):
copy the mjpegtools folder and put it un your project folder

### Usage :

to grab a single frame from mjpeg and save it to disk :
```
from mjpegtools import MjpegParser
image = MjpegParser(url='http://path-to-your-camera-mjpeg').serve()
with open('imagename.jpg', 'wb') as im:
  im.write(image.output.read())
```

to simply grab infinite frames from mjpeg and save it to disk  I would do:
```
from mjpegtools import MjpegParser
from time import time
While True:
  filename = str(time()).replace('.','') + '.' + 'jpeg'
  image = MjpegParser(url='http://path-to-your-camera-mjpeg').serve()
  with open(filename, 'wb') as im:
    im.write(image.output.read())
```

### Website
Use generator.
if you are using Django you can use *HttpResponse*
### flask you can use as_flask_mjpeg:

```
@app.route('/direct-stream')
def stream_direct():
  cam = MjpegParser(url='http://youripadress/videostream.cgi?user=admin&pwd=password&resolution=8&rate=0')
  cam.quality = 20
  return cam.serve().as_flask_mjpeg()
```


CHANGELOG

DEC 28, 2014
- Merged Pull requests (@inactivist)
- Updated pip.
- version changed to 0.0.13
- Added License file

DEC 13, 2014:
- Fix README examples.

JUL 27:
- Tests
- Travis

JUL 23:
- Fixed , now working also with dlink dcs-900

JUL 17 :
- Added four methods => as_image , as_mjpeg, as_flask_mjpeg, as_flask_image
- Performance improvement
- Trying to be as pep8 possible.

JUL 10 :
- converted in to a package
- server renamed to mjpegtools
- updated readme => usage , installation
- registered on

MILESTONE :
- implement a server (I have it in my private repo)
- option to convert realtime to other format.
