#!/usr/bin/env python

import csv
from itertools import imap
import json
import resource
import time

from django.core.management.base import BaseCommand
from django.utils import simplejson as django_json
import simplejson

from serial.models import TestData

class Command(BaseCommand):
    args = '[number of test rows to use]'

    def handle(self, *args, **kwargs):
        n = int(args[0])

        print 'Querying and deserializing %i records' % TestData.objects.all()[:n].count()

        start = time.time()

        for testdata in TestData.objects.all()[:n]:
            json.loads(testdata.json_text)

        end = time.time()
        elapsed = end - start

        print 'stdlib json: %.2f seconds' % elapsed

        start = time.time()

        for testdata in TestData.objects.all()[:n]:
            django_json.loads(testdata.json_text)

        end = time.time()
        elapsed = end - start

        print 'django-simplejson: %.2f seconds' % elapsed

        start = time.time()

        for testdata in TestData.objects.all()[:n]:
            simplejson.loads(testdata.json_text)

        end = time.time()
        elapsed = end - start

        print 'simplejson: %.2f seconds' % elapsed

        start = time.time()

        for testdata in TestData.objects.all()[:n]:
            reader = csv.reader([testdata.csv_text])
            reader.next()

        end = time.time()
        elapsed = end - start

        print 'csv: %.2f seconds' % elapsed

        start = time.time()

        reader = csv.reader([testdata.csv_text for testdata in TestData.objects.all()[:n]])
        
        while True:
            try:
                reader.next()
            except StopIteration:
                break

        end = time.time()
        elapsed = end - start

        print 'csv (list comp): %.2f seconds' % elapsed

        start = time.time()

        reader = csv.reader(imap(lambda n: n.csv_text, TestData.objects.all()[:n]))
        
        while True:
            try:
                reader.next()
            except StopIteration:
                break

        end = time.time()
        elapsed = end - start

        print 'csv (imap): %.2f seconds' % elapsed

