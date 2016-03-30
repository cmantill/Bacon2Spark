#!/usr/bin/env python

from pyspark.sql import Row

class Datum(object):
    @staticmethod
    def convert(x):
        if isinstance(x, Row):
            return Datum.convert(x.asDict())
        elif isinstance(x, dict):
            return Datum(x)
        elif isinstance(x, list):
            return [Datum.convert(v) for v in x]
        else:
            return x
    def __init__(self, asdict):
        for key, value in asdict.items():
            setattr(self, key, Datum.convert(value))
        self._fields = sorted(asdict.keys())
    def __repr__(self):
        return "{" + ", ".join("%s: %r" % (k, getattr(self, k)) for k in self._fields) + "}"
