from unittest import TestCase
from unittest import skip

from models.carousel import Carousel



class CarouselModelTest(TestCase):

    def test_expects_to_instantiate_carousel(self):
        collection = [1, 2, 3]
        carousel = Carousel(collection)
        self.assertIsInstance(carousel, Carousel)
