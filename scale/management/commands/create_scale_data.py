#!/usr/bin/env python

import random
import string

from django.core.management.base import BaseCommand
from django.db import connection, transaction

from scale.models import Dataset, Row

class Command(BaseCommand):
    args = '[number of datasets to create] [number of unique seed rows] [total number of test rows to create] '

    @transaction.commit_manually
    def handle(self, *args, **kwargs):
        cursor = connection.cursor()
        cursor.execute("TRUNCATE TABLE scale_dataset CASCADE")
        cursor.execute("TRUNCATE TABLE scale_row CASCADE")
        transaction.commit()

        i = 0
        datasets = int(args[0])

        while i < datasets:
            d = Dataset.objects.create(
                name=self.random_string(random.randint(0, 100))
                )

            i += 1

        # Get the id of the first dataset created
        transaction.commit()
        print 'Created %i datasets' % datasets
        created_datasets = list(Dataset.objects.all())

        i = 0
        seed_rows = int(args[1]) 

        while i < seed_rows:
            Row.objects.create(
                dataset=random.choice(created_datasets),
                csv_text=self.random_string(random.randint(0, 100))
                )

            i += 1

        transaction.commit()
        print 'Created %i seed rows' % seed_rows

        cursor = connection.cursor()

        print 'Copying seed rows...'
        rows = int(args[2])

        while i < rows:
            cursor.execute("""
                INSERT INTO scale_row (dataset_id, csv_text) (
                SELECT dataset_id, csv_text FROM scale_row LIMIT %i
                )
                """ % seed_rows)
            transaction.commit()

            i += seed_rows

            print '\t%i created' % i

    def random_string(self, n):
        return ''.join(random.choice(string.printable) for i in xrange(n))

