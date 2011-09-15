#!/usr/bin/env python

from datetime import date, datetime, time
from itertools import islice, izip
import sys
from types import NoneType

from django.core.management.base import BaseCommand

import csvkit
from csvkit.exceptions import CustomException, InvalidValueForTypeException
from csvkit.typeinference import normalize_column_type, normalize_table
import sunburnt

class InferredNormalFalsifiedException(CustomException):
    """
    Exception raised when a value with a previously inferred type fails to coerce.
    """
    def __init__(self, row_number, column_name, value, normal_type):
        self.row_number = row_number
        self.column_name = column_name
        self.value = value
        self.normal_type = normal_type
        self.new_type = normalize_column_type([value])[0] 
        msg = 'Row %i, column "%s": Unable to convert "%s" to %s. New type is %s.' % (row_number, column_name, value, normal_type.__name__, self.new_type.__name__)
        super(InferredNormalFalsifiedException, self).__init__(msg)

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        solr = sunburnt.SolrInterface("http://localhost:8983/solr/")

        reader = csvkit.CSVKitReader(open('data/Building_Permits.csv', 'r'))
        headers = reader.next()

        first_hundred = islice(reader, 200)
        normal_types, normal_values = normalize_table(first_hundred, len(headers))

        solr_fields = []

        for h, t in zip(headers, normal_types):
            if t == NoneType:
                solr_fields.append(None)
            else:
                solr_fields.append('%s_%s' % (h, t.__name__))
            
        # Reset reader
        reader = csvkit.CSVKitReader(open('data/Building_Permits.csv', 'r'))
        reader.next()

        buffered = []

        for i, row in enumerate(reader, start=1):
            print i
            data = {}

            for t, header, field, value in izip(normal_types, headers, solr_fields, row):
                try:
                    value = normalize_column_type([value], normal_type=t)[1][0]
                except InvalidValueForTypeException:
                    # Convert exception to row-specific error
                    raise InferredNormalFalsifiedException(i, header, value, t)

                # No reason to send null fields to Solr (also sunburnt doesn't like them) 
                if value == None:
                    continue

                if t in [unicode, bool, int, float]:
                    if value == None:
                        continue

                    data[field] = value
                elif t == datetime:
                    data[field] = value.isoformat()
                elif t == date:
                    pass
                elif t == time:
                    pass
                else:
                    raise TypeError('Unexpected normal type: %s' % t.__name__)

            data['id'] = str(i)
            data['full_text'] = '\n'.join(row)
            buffered.append(data)

            if i % 100 == 0:
                solr.add(buffered)
                buffered = []

        solr.commit()

