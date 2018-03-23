====================
opentracing-pyzipkin
====================

Adapter between opentracing-python and py_zipkin.


Motivation
==========

Currently there are no great options for a Python 3 compatible opentracing
client. py_zipkin (https://github.com/Yelp/py_zipkin) is a Python 3 supporting
zipkin client which closely resembles the OpenTracing API. With minimal effort
we can create an adapter between opentracing-python
(https://github.com/opentracing/opentracing-python) and py_zipkin.
