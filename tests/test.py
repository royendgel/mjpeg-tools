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



if __name__ == '__main__':
    unittest.main()
