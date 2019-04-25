import traceback
import botocore
import boto3
import urllib2

from django.conf import settings


class S3(object):
    def __init__(self, region='ap-southeast-1'):
        self.region = region
        self.bucket = settings.AWS_S3_BUCKET

        session = boto3.Session(
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=region
        )

        self.session = session.resource('s3')

    def create_file(self, key, path):
        """
        Creates file in S3 in default bucket given a local path
        """
        try:
            self.session.Object(self.bucket, key).put(
                ACL='public-read',
                Body=open(path, 'rb'),
            )
            url = "https://s3-{0}.amazonaws.com/{1}/{2}".format(self.region, self.bucket, key)
            return url
        except Exception as e:
            import traceback
            traceback.print_exc()

    def create_file_from_url(self, key, url):
        """
        Creates file in S3 in default bucket given a URL
        """
        try:
            file = urllib2.urlopen(url, timeout=300).read()
            self.session.Object(self.bucket, key).put(
                ACL='public-read',
                Body=file,
            )
            url = "https://s3-{0}.amazonaws.com/{1}/{2}".format(self.region, self.bucket, key)
            return url
        except Exception as e:
            import traceback
            traceback.print_exc()

    def check_file_exists(self, key):
        try:
            self.session.Object(self.bucket, key).load()
            return True
        except:
            return False

    def create_bucket(self, name):
        try:
            self.session.create_bucket(
                Bucket=name.lower(),
                CreateBucketConfiguration={
                    'LocationConstraint': self.region,
                }
            )
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == 'BucketAlreadyOwnedByYou':
                pass
            else:
                print e.response['Error']['Code']
        except Exception as e:
            import traceback
            traceback.print_exc()