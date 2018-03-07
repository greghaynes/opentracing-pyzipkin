import random

from py_zipkin.zipkin import zipkin_span

import span
from _opentracing import tracer as ot_tracer


class Tracer(ot_tracer.Tracer):
    def __init__(self, service_name, sample_rate,
                 transport_handler, port):
        super(Tracer, self).__init__()
        self._service_name = service_name
        self._sample_rate = sample_rate
        self._transport_handler = transport_handler
        self._port = port

        self._random = random.random()

    def start_span(self,
                   operation_name=None,
                   child_of=None,
                   references=None,
                   tags=None,
                   start_time=None):
        pyzk_span = zipkin_span(
            service_name=self._service_name,
            span_name=operation_name,
            transport_handler=self._transport_handler,
            port=self._port,
            sample_rate=self._sample_rate)

        trace_id = None
        parent_id = None
        baggage = None
        if child_of is None:
            trace_id = self._generate_id()
        else:
            trace_id = child_of.trace_id
            parent_id = child_of.span_id
            paggage = child_of.baggage
        span_id = self._generate_id()

        ctxt = span.SpanContext(trace_id, span_id, parent_id, baggage)
        return span.Span(self, ctxt, pyzk_span)

    def _generate_id(self):
        return self._random.getrandbits(64)
