#!/usr/bin/env python

import csv

from django.core.management.base import BaseCommand

import sunburnt

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        solr = sunburnt.SolrInterface("http://localhost:8983/solr/")

        reader = csv.reader(open('data/Building_Permits.csv', 'r'))
        header = reader.next()

        i = 1

        for row in reader:
            data = dict(zip(header, row))
            data['id'] = str(i)
            data['text'] = '\n'.join(row)
            solr.add(data)

            i += 1
            print i

            if i % 500 == 0:

