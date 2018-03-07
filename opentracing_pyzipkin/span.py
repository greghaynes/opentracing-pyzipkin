from urllib import parse as urlparse

from opentracing_pyzipkin._opentracing import span as ot_span
from opentracing_pyzipkin._opentracing import tracer as ot_tracer


_BAGGAGE_PREFIX = '_baggage_'


def carrier_encode(format, val):
    if format == ot_tracer.Format.HTTP_HEADERS:
        ret = val
        if isinstance(val, str):
            ret = urlparse.quote(val.encode('utf-8'))
        return ret


def carrier_decode(format, val):
    if format == ot_tracer.Format.HTTP_HEADERS:
        ret = val
        if isinstance(val, bytes):
            ret = urlparse.unquote(val)
            ret = ret.decode('utf-8')
        return ret


class SpanContext(ot_span.SpanContext):
    @classmethod
    def extract(cls, format, carrier):
        baggage = {}
        for key, val in carrier.items():
            if key.startswith(_BAGGAGE_PREFIX):
                decoded = carrier_decode(format, val)
                baggage[key[len(_BAGGAGE_PREFIX):]] = decoded
        kwargs = {}
        for prop in ('trace_id', 'span_id', 'parent_id'):
            val = carrier_decode(format, carrier[prop])
            if val is not None:
                val = int(val, 16)
            kwargs[prop] = val
        kwargs['baggage'] = baggage
        return SpanContext(**kwargs)

    def __init__(self, trace_id, span_id, parent_id, baggage=None):
        self.trace_id = trace_id
        self.span_id = span_id
        self.parent_id = parent_id
        self._baggage = baggage or ot_span.SpanContext.EMPTY_BAGGAGE

    def __eq__(self, other):
        return (self.trace_id == other.trace_id and
                self.span_id == other.span_id and
                self.parent_id == other.parent_id and
                self.baggage == other.baggage)

    @property
    def baggage(self):
        return self._baggage

    def inject(self, format, carrier):
        for prop in ('trace_id', 'span_id', 'parent_id'):
            val = getattr(self, prop)
            if val is not None:
                val = '%x' % val
            carrier[prop] = carrier_encode(format, val)
        for key, val in self._baggage.items():
            carrier[_BAGGAGE_PREFIX + key] = carrier_encode(format, val)


class Span(ot_span.Span):
    def __init__(self, tracer, context, pyzk_span):
        super(Span, self).__init__(tracer, context)
        self._pyzk_span = pyzk_span

    def __enter__(self):
        self._pyzk_span.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        super(Span, self).__exit__(exc_type, exc_val, exc_tb)
        self._pyzk_span.__exit__(exc_type, exc_val, exc_tb)

    def __eq__(self, other):
        return self.context == other.context
