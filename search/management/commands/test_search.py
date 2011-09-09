#!/usr/bin/env python

import random
import time

from django.core.management.base import BaseCommand

from scale.models import Dataset, Row

class Command(BaseCommand):
    args = '[number of datasets to create] [number of unique seed rows] [total number of test rows to create] '

    def __init__(self):
        self.datasets = 0
        self.rows = 0

    def handle(self, *args, **kwargs):
        self.datasets = Dataset.objects.all().count()
        self.rows = Row.objects.all().count()
        print 'Testing with %i datasets and %i rows' % (self.datasets, self.rows)

        tests = ['test_count_datasets', 'test_count_rows', 'test_dataset_first_hundred_rows', 'test_random_access']
        random.shuffle(tests)

        for func in tests:
            start = time.time()

            getattr(self, func)()

            end = time.time()
            elapsed = end - start

            print '%s\t\t\t%ims' % (func, elapsed * 1000)

    def test_count_datasets(self):
        c = Dataset.objects.all().count()

    def test_count_rows(self):
        c = Row.objects.all().count()

    def test_dataset_first_hundred_rows(self):
        d = Dataset.objects.all()[0]
        r = d.rows.all()[:100]

    def test_random_access(self):
        i = random.randint(0, 20000000)
        Row.objects.get(id=i)

