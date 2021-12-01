from unittest import TestCase
from screen import Screen

class TestScreen(TestCase):
    def test_single_capture(self):
        screen = Screen(0, 0, 1920, 1080)
        image = screen.getScreen()
        assert len(image.shape) == 3
        assert image.shape == (1080, 1920, 3)

    def test_too_large_capture(self):
        screen = Screen(0, 0, 10000, 10000)
        image = screen.getScreen()
        assert len(image.shape) == 3
        assert image.shape == (10000, 10000, 3)

    def test_repeated_capture(self):
        screen = Screen(0, 0, 1920, 1080)
        for i in range(100):
            screen.updateScreen()
            image = screen.getScreen()
            assert image is not None
            assert image.shape == (1080, 1920, 3)


