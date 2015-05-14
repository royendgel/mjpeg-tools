import os
import unittest
from mjpegtools import MjpegParser

class TestMjpegTools(unittest.TestCase):

  def setUp(self):
    self.url = 'file://' + os.path.join(os.path.dirname(os.path.realpath(__file__)),'fixtures','simple.mjpg')

  # Get single image
  def get_single_image(self, quality=50):
    image = MjpegParser(url=self.url)
    image.quality= quality
    return image.serve().as_image()


  def test_single_image_parser(self):
    image = self.get_single_image()
    image.seek(0,os.SEEK_END); lenimg=image.tell()
    self.assertIsNot(0, lenimg)

  def test_single_image_different_quality(self):
    # Test different sizes of image
    image1 = self.get_single_image(quality=50)
    image2 = self.get_single_image(quality=80)
    image3 = self.get_single_image(quality=20)
    image4 = self.get_single_image(quality=50)
    
    image1.seek(0, os.SEEK_END); len1=image1.tell()
    image2.seek(0, os.SEEK_END); len2=image2.tell()
    image3.seek(0, os.SEEK_END); len3=image3.tell()
    image4.seek(0, os.SEEK_END); len4=image4.tell()
    self.assertIsNot(len1, len2)
    self.assertIsNot(len2, len3)
    self.assertIsNot(len1, len3)
    self.assertEqual(len1, len4)

  def test_camera_ping_wrong(self):
    wrong_url = MjpegParser(url=self.url + 'wrong-url')
    self.assertFalse(wrong_url.ping, msg="The Camera url is correct \
    it should not be ")

  def test_camera_ping_correct(self):
    correct_url = MjpegParser(url=self.url)
    self.assertTrue(correct_url.ping, msg="The camera url is not \
     correct it should be")

if __name__ == '__main__':
    unittest.main()
