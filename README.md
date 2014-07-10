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
  im.write(image.read())
```

to simply grab infinite frames from mjpeg and save it to disk  I would do:
```
from mjpegtools import MjpegParser
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
### flask you can use *Response* I did:

`
@app.route('/direct-stream')
def stream_direct():
  cam = MjpegParser(url='http://youripadress/videostream.cgi?user=admin&pwd=password&resolution=8&rate=0')
  cam.quality = 20
  def generate():
    while True:
      c = cam.serve()
      # yield cam.data # you can use this if you are not manipulating the image
      yield '\r\n'
      yield '--ipcamera\r\n'
      yield 'Content-Length: ' + str(cam.length) + '\r\n'
      yield 'Content-Type: image/jpeg\r\n'
      yield '\r\n'
      yield c.read()

  resp = Response(generate(), mimetype='image/jpeg',content_type='multipart/x-mixed-replace;boundary=ipcamera',direct_passthrough=True)
  return resp
  `


CHANGELOG
JUL 10 :
- converted in to a package
- server renamed to mjpegtools
- updated readme => usage , installation
- registered on

MILESTONE :
- implement a server (I have it in my private repo)
- option to convert realtime to other format.
