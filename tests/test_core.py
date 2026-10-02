import math
from types import SimpleNamespace
import unittest
from unittest.mock import MagicMock, patch
from app import posture_measure
from common import open_camera
from desenho import distance

class CoreTests(unittest.TestCase):
    def test_posture_distance_and_low_visibility(self):
        points = [SimpleNamespace(y=0.2, visibility=1.0) for _ in range(33)]
        points[11].y = points[12].y = 0.48
        self.assertAlmostEqual(posture_measure(points), 0.28)
        points[7].visibility = 0.1
        self.assertIsNone(posture_measure(points))
        points[7].visibility = 1
        points[8].y = math.nan
        self.assertIsNone(posture_measure(points))

    def test_distance_respects_frame_dimensions(self):
        a, b = SimpleNamespace(x=0, y=0), SimpleNamespace(x=0.3, y=0.4)
        self.assertAlmostEqual(distance(a, b, 100, 100), 50)

    @patch('common.cv2.VideoCapture')
    def test_failed_camera_is_released(self, capture):
        camera = MagicMock()
        camera.isOpened.return_value = True
        camera.read.return_value = (False, None)
        capture.return_value = camera
        with self.assertRaises(RuntimeError):
            open_camera(0)
        camera.release.assert_called_once()

    @patch.dict('os.environ', {'CAMERA_INDEX': 'invalid'})
    @patch('common.cv2.VideoCapture')
    def test_invalid_index_does_not_open_camera(self, capture):
        with self.assertRaises(ValueError):
            open_camera()
        capture.assert_not_called()

if __name__ == '__main__':
    unittest.main()
