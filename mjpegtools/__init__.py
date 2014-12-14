import urllib2
import io
import re
import time
import StringIO
import logging
from base64 import b64encode

class MjpegParser(object):
  def __init__(self, url, auth=None, timeout=2):
    """
    :param url: The url
    :param auth: A tuple containing username, password for basic
                 auth, or none if no auth needed.
    :param timeout: The timeout value for urllib.urlopen().
    """
    self.pil = True
    self.quality = 50
    self.format = 'jpeg'
    self.timeout= timeout
    request = urllib2.Request(url)
    try:
      if auth:
        request.add_header('Authorization', 'Basic ' + b64encode(auth[0] + ':' + auth[1]) )
      self.input = urllib2.urlopen(request, timeout=self.timeout)
      self.ping = True
    except:
      logging.error('input error')
      self.ping = False

    self.length = 0
    # Mimic the same data as the origin input, good if you are streaming as-is.
    self.data = ''
    self.headers = self.get_headers()


  # Default headers when serving to the client as mjpeg
  def get_headers(self):
    return '\r\n' + '--ipcamera\r\n' + 'Content-Length: ' + str(self.length) + \
    '\r\n' + 'Content-Type: image/jpeg\r\n' + '\r\n'

  def serve(self):
    # Regex for digits in content-length.
    regex = re.compile("\d+")
    # Declare some empty vars with init values for while loop.
    content_length = 0
    content_type = 0
    content = ''
    self.data = ''


    # loop until it contains: content_length and content-type
    while content_length == 0 or content_type == 0:
      # Pick up the content-length.
      if 'content-length' in content.lower():
        length = regex.findall(content)
        if len(length) >= 1:
          content_length = int(length[0])
          self.length = content_length
      if 'content-type' in content.lower():
        content_type = 1

      # Nothing found startover.
      content = self.input.readline()

    data = self.input.read(content_length)
    self.data += content # Slow need to use join instead (pep8 Style).
    self.output = StringIO.StringIO()
    self.length = self.output.len
    self.filename = 'cameraphoto.jpg'

    # if pil is enabled (by default enabled).
    if self.pil:
      from PIL import Image
      self.im = Image.open(io.BytesIO(data))
      # If you need to do more changes to the image.
      # Use overide the image_manipulator.
      self.image_manipulator(self.im)
      self.im.save(self.output, format=self.format, quality=self.quality)
      self.output.seek(0)

    else:
      self.output.write(data)
      self.output.seek(0)
    self.length = self.output.len
    return self

  # Overide this method to do more image manipulations.
  def image_manipulator(self, image):
    '''You can manipulate your image here in example :
    from PIL import ImageDraw
    draw = ImageDraw.Draw(self.im)
    draw.text((0, 0), str(time.ctime()) + " Your Camera name : " \
    , (255, 255, 255))
    '''
    pass

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

  def as_flask_image(self):
    from flask import send_file
    return send_file(self.output,
                     attachment_filename=self.filename,
                     as_attachment=True)

  def as_image(self):
    return self.output
