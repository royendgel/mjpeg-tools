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
    self.assertIsNot(0, image.len)

  def test_single_image_different_quality(self):
    # Test different sizes of image
    image1 = self.get_single_image(quality=50)
    image2 = self.get_single_image(quality=80)
    image3 = self.get_single_image(quality=20)
    image4 = self.get_single_image(quality=50)
    self.assertIsNot(image1.len, image2.len)
    self.assertIsNot(image2.len, image3.len)
    self.assertIsNot(image1.len, image3.len)
    self.assertEqual(image1.len, image4.len)

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
