import unittest

from orbit import ring_gap


class RingGapTest(unittest.TestCase):
    def test_base_gap(self):
        self.assertEqual(ring_gap(0), 40)

    def test_gap_grows_with_speed(self):
        self.assertGreater(ring_gap(10), ring_gap(5))


if __name__ == "__main__":
    unittest.main()
