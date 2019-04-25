import pandas as pd
import os
import sys
import subprocess
import urllib2
import traceback
from multiprocessing import Pool
from elasticsearch_dsl import connections
import elasticsearch
import certifi

from django.core.management.base import BaseCommand
from django.conf import settings
from app.core.models import Document
from app.core.helpers.s3 import S3
from app.core.elastic import ESDocument


def index(doc):
    try:
        # Get the URL of the main document depending on exchange
        ex = doc.company.exchange_id
        if ex == 1:
            input_url = doc.meta['txt']
        elif ex == 5 or ex == 6 or ex == 7 or ex == 8:
            input_url = doc.meta['1']['cached_url']

        # Start indexing
        print 'Indexing {}'.format(input_url)
        sys.stdout.flush()

        input_file = urllib2.urlopen(input_url, timeout=300)
        body = input_file.read().decode('utf-8', 'ignore')

        cat_name = None
        cat_type = None

        if doc.cat:
            cat_name = doc.cat.name
            cat_type = doc.cat.type

        search_doc = ESDocument.get(id=doc.id)
        search_doc.update(
            ticker=doc.company.ticker,
            created_at=doc.date,
            description=doc.description,
            cat=cat_name,
            body=body,
            size=doc.size,
            type=cat_type,
            url=doc.url,
        )
    except elasticsearch.NotFoundError:
        search_doc = ESDocument(
            id=doc.id,
            ticker=doc.company.ticker,
            created_at=doc.date,
            description=doc.description,
            cat=cat_name,
            body=body,
            size=doc.size,
            type=cat_type,
            url=doc.url,
        )
        search_doc.save()
    except Exception as e:
        print 'Error {}: {}'.format(doc.id, e)
        sys.stdout.flush()

    doc.meta['indexed'] = True
    doc.save()


class Command(BaseCommand):
    help = ('Index documents for ticker')

    def add_arguments(self, parser):
        parser.add_argument('-t', '--ticker', help='Ticker', required=False)
        parser.add_argument('-r', '--reindex', help='Reindex', action='store_true')

    def handle(self, *args, **options):
        ticker = options['ticker']
        reindex = options['reindex']
        # self.pool = Pool(processes=10)

        res = connections.create_connection(
            hosts=[settings.ES_HOST],
            http_auth=(settings.ES_USER, settings.ES_PASSWORD),
            use_ssl=settings.ES_USE_SSL,
            ca_certs=certifi.where(),
        )
        print res

        ESDocument.init()

        docs = Document.objects.filter(company__ticker=ticker, meta__isnull=False)
        for doc in docs:
            try:
                if (reindex or not 'indexed' in doc.meta) and 'txt' in doc.meta:
                    # self.pool.apply_async(index, (doc,))
                    index(doc)
            except Exception as e:
                traceback.print_exc()

        # self.pool.close()
