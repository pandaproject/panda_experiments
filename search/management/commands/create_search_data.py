#!/usr/bin/env python

from datetime import date, datetime, time
from itertools import islice
import sys
from types import NoneType

from django.core.management.base import BaseCommand

import csvkit
from csvkit.typeinference import normalize_column_type, normalize_table
import sunburnt

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        solr = sunburnt.SolrInterface("http://localhost:8983/solr/")

        reader = csvkit.CSVKitReader(open('data/Building_Permits.csv', 'r'))
        header = reader.next()

        first_hundred = islice(reader, 200)
        normal_types, normal_values = normalize_table(first_hundred, len(header))

        solr_fields = []

        for h, t in zip(header, normal_types):
            if t == NoneType:
                solr_fields.append(None)
            else:
                solr_fields.append('%s_%s' % (h, t.__name__))
            
        # Reset reader
        reader = csvkit.CSVKitReader(open('data/Building_Permits.csv', 'r'))
        reader.next()

        buffered = []

        for i, row in enumerate(reader):
            print i
            data = {}

            for t, field, value in zip(normal_types, solr_fields, row):
                value = normalize_column_type([value], normal_type=t)[1][0]

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

            if i % 500 == 0:
                solr.add(buffered)
                buffered = []

        solr.commit()

