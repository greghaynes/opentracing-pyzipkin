import unittest

import tracer


class TestTracer(unittest.TestCase):
    def test_init(self):
        t = tracer.Tracer('test', 100, None, 9999)

    def test_start_span(self):
        encoded_spans = []
        def transport_handler(encoded_span):
            encoded_spans.append(encoded_span)

        t = tracer.Tracer('test', 100, transport_handler, 9999)
        with t.start_span('test_op') as span:
            pass

        self.assertEqual(1, len(encoded_spans))

        encoded_spans = []
        with t.start_span('outer_op') as outer_span:
            with t.start_span('inner_op', outer_span) as inner_span:
                pass

        self.assertEqual(2, len(encoded_spans))

    def test_inject(self):
        encoded_spans = []
        def transport_handler(encoded_span):
            encoded_spans.append(encoded_span)

        t = tracer.Tracer('test', 100, transport_handler, 9999)
        with t.start_span('test_op') as span:
            carrier = {}
            t.inject(span.context, tracer.Format.HTTP_HEADERS, carrier)

            new_span = t.extract(tracer.Format.HTTP_HEADERS, carrier)
            self.assertEqual(span.context, new_span)
