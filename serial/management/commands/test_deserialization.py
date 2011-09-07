#!/usr/bin/env python

import csv
import json
import time

from django.core.management.base import BaseCommand
from django.utils import simplejson as django_json
import simplejson

from serial.models import TestData

class Command(BaseCommand):
    args = '[number of test rows to create]'

    def handle(self, *args, **kwargs):
        print 'Derializing json with stdlib'
        start = time.time()

        for testdata in TestData.objects.all():
            json.loads(testdata.json_text)

        end = time.time()
        elapsed = end - start

        print 'Finished in %.2f seconds' % elapsed

        print 'Derializing json with django simplejson'
        start = time.time()

        for testdata in TestData.objects.all():
            django_json.loads(testdata.json_text)

        end = time.time()
        elapsed = end - start

        print 'Finished in %.2f seconds' % elapsed

        print 'Derializing json with simplejson'
        start = time.time()

        for testdata in TestData.objects.all():
            simplejson.loads(testdata.json_text)

        end = time.time()
        elapsed = end - start

        print 'Finished in %.2f seconds' % elapsed

        print 'Derializing csv'
        start = time.time()


        for testdata in TestData.objects.all():
            reader = csv.reader([testdata.csv_text])
            reader.next()

        end = time.time()
        elapsed = end - start

        print 'Finished in %.2f seconds' % elapsed

