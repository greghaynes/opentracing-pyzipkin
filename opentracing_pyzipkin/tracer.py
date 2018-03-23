import random

from py_zipkin.zipkin import zipkin_span, ZipkinAttrs

from opentracing_pyzipkin import span
from opentracing_pyzipkin._opentracing import tracer as ot_tracer


Format = ot_tracer.Format


class Tracer(ot_tracer.Tracer):
    def __init__(self, service_name, sample_rate,
                 transport_handler, port):
        super(Tracer, self).__init__()
        self._service_name = service_name
        self._sample_rate = sample_rate
        self._transport_handler = transport_handler
        self._port = port

        random.seed()

    def start_span(self,
                   operation_name=None,
                   child_of=None,
                   references=None,
                   tags=None,
                   start_time=None):

        trace_id = None
        parent_id = None
        baggage = None
        parent_id_str = None
        if child_of is None:
            trace_id = self._generate_id()
        else:
            parent = child_of.context
            trace_id = parent.trace_id
            parent_id = parent.span_id
            parent_id_str = '{:016x}'.format(parent_id)
            paggage = parent.baggage
        span_id = self._generate_id()

        zattrs = ZipkinAttrs('{:016x}'.format(trace_id),
                             '{:016x}'.format(span_id),
                             parent_id_str,
                             '0', True)
        pyzk_span = zipkin_span(
            service_name=self._service_name,
            zipkin_attrs=zattrs,
            span_name=operation_name,
            transport_handler=self._transport_handler,
            port=self._port,
            sample_rate=self._sample_rate)

        ctxt = span.SpanContext(trace_id, span_id, parent_id, baggage)
        return span.Span(self, ctxt, pyzk_span)

    def inject(self, span_context, format, carrier):
        span_context.inject(format, carrier)

    def extract(self, format, carrier):
        return span.SpanContext.extract(format, carrier)

    def _generate_id(self):
        return random.getrandbits(64)

child_of = ot_tracer.child_of
