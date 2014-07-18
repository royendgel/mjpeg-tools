import urllib2
import io
import re
import time
import StringIO

class MjpegParser(object):
  def __init__(self, url, **kwargs):
    # for now it's always true
    self.pil = True
    self.quality = 50
    self.format = 'jpeg'
    self.input = urllib2.urlopen(url)
    self.length = 0
    # mimic the same data
    self.data = ''
    self.headers = self.get_headers()

  def get_headers(self):
    return '\r\n' + '--ipcamera\r\n' + 'Content-Length: ' + str(self.length) +  '\r\n' + 'Content-Type: image/jpeg\r\n' + '\r\n'

  def serve(self):
    while True:
      regex = re.compile("\d+")
      content_length = 0
      content = ''
      self.data = ''
      while content_length == 0:
        if 'Content-Length'.lower() in content.lower():
          length = regex.findall(content)
          if len(length) >= 1:
            content_length = int(length[0])
            self.length = content_length
        content = self.input.readline()
        data = self.input.read(content_length)
        self.data += content # Slow need to use join instead (pep8 Style)

      if self.pil:
          from PIL import Image
          self.output = StringIO.StringIO()
          im = Image.open(io.BytesIO(data))
          im.save(self.output, format=self.format, quality=self.quality)
          self.output.seek(0)
          # it return file-like object in memory
          self.length = self.output.len
          return self

  def as_mjpeg(self):
    def generate():
      while True:
        cam = self.serve()
        c = cam.output
        yield self.get_headers()
        yield c.read()
    return generate()

  def as_flask_mjpeg(self):
    def generate():
      while True:
        cam = self.serve()
        c = cam.output
        yield self.get_headers()
        yield c.read()
    from flask import Response
    resp = Response(generate(), mimetype='image/jpeg',\
    content_type='multipart/x-mixed-replace;boundary=ipcamera',\
    direct_passthrough=True)
    return resp

  def as_image(self):
    return self.output
