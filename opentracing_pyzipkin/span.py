from _opentracing import span as ot_span


class SpanContext(ot_span.SpanContext):
    def __init__(self, trace_id, span_id, parent_id, baggage=None):
        self.trace_id = trace_id
        self.span_id = span_id
        self.parent_id = parent_id
        self._baggage = baggage or ot_span.SpanContext.EMPTY_BAGGAGE

    @property
    def baggage(self):
        return self._baggage


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
