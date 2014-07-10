import urllib2
import io
import re
import time
import StringIO

from PIL import Image

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
        self.data += content

      if self.pil:
          output = StringIO.StringIO()
          im = Image.open(io.BytesIO(data))
          im.save(output, format=self.format, quality=self.quality)
          output.seek(0)
          # it return file-like object in memory
          self.length = output.len
          return output
