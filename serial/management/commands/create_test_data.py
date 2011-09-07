#!/usr/bin/env python

import csv
import random
import string
import StringIO

from django.core.management.base import BaseCommand
import simplejson

from serial.models import TestData

class Command(BaseCommand):
    args = '[number of test rows to create]'

    def handle(self, *args, **kwargs):
        i = 0
        rows = int(args[0])

        while i < rows:
            data = {}
            j = 0
            columns = random.randint(0, 100)
            names = []

            while j < columns:
                k = self.random_string(random.randint(0, 100))
                v = self.random_string(random.randint(0, 100))
                names.append(k)
                data[k] = v

                j += 1

            json_text = simplejson.dumps(data)
            csv_stringio = StringIO.StringIO()
            csv_writer = csv.DictWriter(csv_stringio, fieldnames=names)
            csv_writer.writerow(data)
            csv_text = csv_stringio.getvalue()

            TestData.objects.create(
                json_text=json_text,
                csv_text=csv_text)

            i += 1

    def random_string(self, n):
        return ''.join(random.choice(string.printable) for i in xrange(n))

