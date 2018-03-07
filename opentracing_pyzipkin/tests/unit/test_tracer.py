import tracer

import unittest


class TestTracer(unittest.TestCase):
    def test_init(self):
        t = tracer.Tracer('test', 100, None, 9999)
