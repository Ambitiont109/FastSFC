import pandas as pd
import os
import sys
import subprocess
import urllib2
import traceback
from multiprocessing import Pool

from django.core.management.base import BaseCommand
from app.core.management.commands.search import index
from django.conf import settings
from app.core.models import Document, Company
from app.core.helpers.s3 import S3


def convert_file(ticker, doc, input_path, output_path, filetype):
    try:
        print 'Converting file: {}'.format(input_path)
        sys.stdout.flush()

        if not os.path.isfile(output_path):
            subprocess.check_call(['pdf2txt.py', '-o', output_path, '-t', filetype, input_path])

        key = ticker + '/' + output_path[output_path.rfind("/")+1:]
        url = S3().create_file(key, output_path)

        doc.refresh_from_db()
        if not doc.meta:
            doc.meta = {}

        # use txt instead of text as key
        filetype = filetype.replace('text', 'txt')
        doc.meta[filetype] = url
        doc.save()

        # if doc is not indexed, add to elastic
        if 'txt' in doc.meta and 'indexed' not in doc.meta:
            index(doc)

        print 'Created {}'.format(output_path)
    except Exception as e:
        print 'Failed to create doc {}: {}'.format(doc.id, e)


def save_file(doc, key, path, filetype):
    try:
        print 'Saving file: {}'.format(path)
        sys.stdout.flush()

        url = S3().create_file(key, path)

        doc.refresh_from_db()
        if not doc.meta:
            doc.meta = {}

        doc.meta[filetype] = url
        doc.save()
    except Exception as e:
        print 'Failed to save doc {}: {}'.format(doc.id, e)


class Command(BaseCommand):
    help = ('Parse PDF documents')
    asset_root = '../assets/'

    def add_arguments(self, parser):
        # Only parse documents for a specified ticker
        parser.add_argument('-t', '--ticker', help='Ticker', required=False)

        # Only parse documents where meta is empty
        parser.add_argument('-n', '--new', help='New', required=False, action='store_true')

    def parse(self, ticker):
        if self.new:
            print '\033[44mParsing new docs for ticker {}...\033[0m'.format(ticker)
            docs = Document.objects.filter(company__ticker=ticker, meta__isnull=True)
        else:
            print '\033[44mParsing all docs for ticker {}...\033[0m'.format(ticker)
            docs = Document.objects.filter(company__ticker=ticker)

        for doc in docs:
            try:
                print 'Start parsing doc {}'.format(doc.url)
                base_url = self.asset_root + ticker + '/'
                filename_ext = doc.url[doc.url.rfind("/")+1:]
                filename, ext = os.path.splitext(filename_ext)

                if not os.path.exists(base_url):
                    os.mkdir(base_url)

                input_file = base_url + filename_ext
                output_html = base_url + filename + '_processed.html'
                output_txt = base_url + filename + '_processed.txt'

                input_file_key = ticker + '/' + filename_ext
                output_html_key = ticker + '/' + filename + '_processed.html'
                output_txt_key = ticker + '/' + filename + '_processed.txt'

                input_file_exists = os.path.isfile(input_file)

                if doc.meta:
                    if ext.lower() == '.pdf' and 'pdf' in doc.meta and 'html' in doc.meta and 'text' in doc.meta:
                        print 'Skip {} {}'.format(ext.lower(), doc.url)
                        # If PDF, we want to store PDF, HTML and TXT version in S3. Skip if already stored
                        continue
                    elif ext[1:].lower() in doc.meta:
                        print 'Skip {} {}'.format(ext.lower(), doc.url)
                        # If not PDF, we want to store the original file in S3. Skip if already stored
                        continue

                if not input_file_exists:
                    print 'Downloading {}'.format(doc.url)
                    file = urllib2.urlopen(doc.url, timeout=300)
                    with open(input_file, 'wb') as output:
                        output.write(file.read())

                # upload original file to S3
                if not S3().check_file_exists(input_file_key):
                    filetype = ext[1:].lower()
                    self.pool.apply_async(save_file, (doc, input_file_key, input_file, filetype))

                # if pdf, convert it to html and upload to S3
                if ext.lower() == '.pdf' and not S3().check_file_exists(output_html_key):
                    self.pool.apply_async(convert_file, (ticker, doc, input_file, output_html, 'html'))

                # if pdf, convert it to txt and upload to S3
                if ext.lower() == '.pdf' and not S3().check_file_exists(output_txt_key):
                    self.pool.apply_async(convert_file, (ticker, doc, input_file, output_txt, 'text'))

            except Exception as e:
                traceback.print_exc()

    def handle(self, *args, **options):
        self.ticker = options['ticker']
        self.new = options['new']

        # Create local asset directory if it does not exist
        if not os.path.exists(self.asset_root):
            os.mkdir(self.asset_root)

        # Create S3 bucket
        S3().create_bucket(settings.AWS_S3_BUCKET)

        # Start pool
        self.pool = Pool(processes=20)

        if self.ticker:
            companies = Company.objects.filter(ticker=ticker)
        else:
            # Only select HKEx companies
            companies = Company.objects.filter(exchange_id=1)

        for company in companies:
            self.parse(company.ticker)

        self.pool.close()
