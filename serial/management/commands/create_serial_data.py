#!/usr/bin/env python

import csv
import random
import string
import StringIO

from django.core.management.base import BaseCommand
from django.db import transaction
import simplejson

from serial.models import TestData

class Command(BaseCommand):
    args = '[number of test rows to create]'

    @transaction.commit_manually
    def handle(self, *args, **kwargs):
        TestData.objects.all().delete()
        transaction.commit()

        i = 0
        rows = int(args[0])

        while i < rows:
            data = []
            j = 0
            columns = random.randint(0, 100)

            while j < columns:
                data.append(self.random_string(random.randint(0, 100)))

                j += 1

            json_text = simplejson.dumps(data)
            csv_stringio = StringIO.StringIO()
            csv_writer = csv.writer(csv_stringio)
            csv_writer.writerow(data)
            csv_text = csv_stringio.getvalue()

            TestData.objects.create(
                json_text=json_text,
                csv_text=csv_text)

            i += 1

            if i % 1000 == 0:
                print 'Created %i' % i
                transaction.commit()

    def random_string(self, n):
        return ''.join(random.choice(string.printable) for i in xrange(n))

