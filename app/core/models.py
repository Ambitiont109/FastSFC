from django.db import models
from django.core.urlresolvers import reverse
from jsonfield import JSONField
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    meta = JSONField(null=True)


class Watchlist(models.Model):
    company = models.ForeignKey('core.Company', null=False, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    meta = JSONField(null=True)


class Period (models.Model):
    short_name = models.CharField(max_length=10, null=True)

    def __unicode__(self):
        return self.short_name


class DocumentCategory (models.Model):
    name = models.CharField(max_length=200, null=False)
    type = models.CharField(max_length=200, null=False, default="other", db_index=True)
    description = models.CharField(max_length=1000, null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Document Categories"


class DocumentSubcategory (models.Model):
    name = models.CharField(max_length=1000, null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Document Subcategories"


class Exchange (models.Model):
    short_name = models.CharField(max_length=20, null=True)
    full_name = models.CharField(max_length=100, null=True)

    def __unicode__(self):
        return self.short_name


class Company (models.Model):
    ticker = models.CharField(max_length=10, null=True, db_index=True)
    ticker_alt = models.CharField(max_length=100, null=True)
    exchange = models.ForeignKey('core.Exchange', null=True)
    full_name = models.CharField(max_length=200, null=True)
    full_alt_name = models.CharField(max_length=500, null=True)
    industry = models.ForeignKey('core.Industry', null=True)
    meta = JSONField(null=True)
    short_alt_name = models.CharField(max_length=100, null=True, db_index=True, unique=True)
    short_name = models.CharField(max_length=200, null=True, db_index=True)
    website = models.URLField(null=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.ticker

    def get_absolute_url(self):
        return reverse('core:company_document', kwargs={'ticker': self.ticker})

    def website_url(self):
        if self.website:
            return '<a href="%s">%s</a>' % (self.website, self.website)
        else:
            return ''

    def get_layout(self):
        if self.exchange.short_name == 'NYSE' \
        or self.exchange.short_name == 'NASDAQ' \
        or self.exchange.short_name == 'AMEX':
            return 'us'

        return 'hk'

    def get_latest_document(self):
        try:
            return Document.objects.filter(company__ticker=self.ticker).order_by('-date')[0]
        except:
            return None

    def get_document_count(self):
        try:
            return Document.objects.filter(company__ticker=self.ticker).count()
        except:
            return 0

    website_url.allow_tags = True

    class Meta:
        verbose_name_plural = "Companies"


class Document (models.Model):
    FILETYPES = (
        ('PDF', 'PDF'),
        ('HTML', 'HTML'),
        ('HTM', 'HTM'),
        ('PPT', 'PPT'),
        ('DOC', 'DOC'),
        ('Multiple', 'Multiple'),
    )

    cat = models.ForeignKey('core.DocumentCategory', null=True)
    company = models.ForeignKey('core.Company', null=True)
    subcat = models.ForeignKey('core.DocumentSubcategory', null=True)
    date = models.DateTimeField(null=True, db_index=True)
    description = models.CharField(max_length=1000, null=True)
    filetype = models.CharField(max_length=20, choices=FILETYPES, null=True)
    indexed = models.BooleanField(default=False, null=False)
    last_updated = models.DateTimeField(auto_now=True)
    meta = JSONField(null=True)
    ref = models.CharField(max_length=50, null=True)
    size = models.IntegerField(null=True)
    url = models.URLField(null=True)

    def document_url(self):
        if self.url:
            return '<a href="%s">%s</a>' % (self.url, self.url)
        else:
            return ''

    document_url.allow_tags = True


class WebsiteDocument (models.Model):
    company = models.ForeignKey('core.Company', null=True)
    url = models.URLField(null=True)
    description = models.CharField(max_length=1000, null=True)
    last_updated = models.DateTimeField(auto_now=True)


class DocumentCount (models.Model):
    company = models.ForeignKey('core.Company', null=False)
    actual_count = models.IntegerField(null=True)
    our_count = models.IntegerField(null=True)

    class Meta:
        verbose_name_plural = "Document Counts"


class Price (models.Model):
    company = models.ForeignKey('core.Company', null=True)
    date = models.DateTimeField(null=True, db_index=True)
    open = models.FloatField(null=True)
    high = models.FloatField(null=True)
    low = models.FloatField(null=True)
    close = models.FloatField(null=True)
    adj_close = models.FloatField(null=True)
    volume = models.FloatField(null=True)


class Industry (models.Model):
    industry = models.CharField(max_length=100, null=True)
    supersector = models.CharField(max_length=100, null=True)
    sector = models.CharField(max_length=100, null=True)
    subsector = models.CharField(max_length=100, null=True)
    code = models.CharField(max_length=10, null=True)


class Source (models.Model):
    name = models.CharField(max_length=255, null=False, unique=True, db_index=True)
    description = models.CharField(max_length=1000, null=True)

    def __unicode__(self):
        return self.name


class Metric (models.Model):
    name = models.CharField(max_length=255, null=False, unique=True, db_index=True)
    source = models.ForeignKey('core.Source', null=True, default=None)
    description = models.CharField(max_length=1000, null=True)
    type = models.CharField(max_length=20, null=True)
    meta = JSONField(null=True)

    def __unicode__(self):
        return self.name

    def timeseriesCount(self):
        return Timeseries.objects.filter(metric_id__exact=self.id).count()


class Timeseries (models.Model):
    metric = models.ForeignKey('core.Metric', null=False)
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)
    type = models.CharField(max_length=20, null=True)
    value = models.FloatField(null=True)
    get_latest_by = 'date'
