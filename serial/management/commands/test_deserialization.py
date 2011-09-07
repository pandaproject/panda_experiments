#!/usr/bin/env python

import csv
from itertools import imap
import json
import random
import resource
import time

from django.core.management.base import BaseCommand
from django.utils import simplejson as django_json
import simplejson

from serial.models import TestData

class Command(BaseCommand):
    args = '[number of test rows to use]'

    def __init__(self):
        self.last_mem = 0

    def handle(self, *args, **kwargs):
        n = int(args[0])
        print 'Querying and deserializing %i records' % TestData.objects.all()[:n].count()
        print 'Initial memory usage: %i' % self.get_new_memory_usage()

        tests = ['test_stdlib_json', 'test_django_json', 'test_simplejson', 'test_csv', 'test_csv_list_comp', 'test_csv_imap']
        random.shuffle(tests)

        for func in tests:
            start = time.time()

            getattr(self, func)(n)

            end = time.time()
            elapsed = end - start

            print '%s\t\t\t%.2fs\t\t%i' % (func, elapsed, self.get_new_memory_usage())

    def test_stdlib_json(self, n):
        for testdata in TestData.objects.all()[:n]:
            json.loads(testdata.json_text)

    def test_django_json(self, n):
        for testdata in TestData.objects.all()[:n]:
            django_json.loads(testdata.json_text)

    def test_simplejson(self, n):
        for testdata in TestData.objects.all()[:n]:
            simplejson.loads(testdata.json_text)

    def test_csv(self, n):
        for testdata in TestData.objects.all()[:n]:
            reader = csv.reader([testdata.csv_text])
            reader.next()

    def test_csv_list_comp(self, n):
        reader = csv.reader([testdata.csv_text for testdata in TestData.objects.all()[:n]])
        
        while True:
            try:
                reader.next()
            except StopIteration:
                break

    def test_csv_imap(self, n):
        reader = csv.reader(imap(lambda n: n.csv_text, TestData.objects.all()[:n]))
        
        while True:
            try:
                reader.next()
            except StopIteration:
                break

    def get_new_memory_usage(self):
        stats = resource.getrusage(resource.RUSAGE_SELF)
        new_mem = stats[2] - self.last_mem
        self.last_mem = stats[2]
        return new_mem

