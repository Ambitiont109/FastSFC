import math
import urllib
from datetime import datetime, timedelta

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic import View, ListView
from django.shortcuts import render
from django.db.models import Q

from app.core.models import Company, Document, WebsiteDocument
from app.core.elastic import ESDocument


class CompanyDocumentCategorized(ListView):
    def get(self, request, ticker):
        try:
            if ticker.isdigit():
                company = Company.objects.get(id=ticker)
            else:
                company = Company.objects.get(ticker=ticker)

            layout = company.get_layout()
            financials = Document.objects.filter(
                company=company,
                cat__type='financials'
            ).order_by('-date')[:9]

            announcements = Document.objects.filter(
                company=company,
                cat__type='announcements'
            ).order_by('-date')[:9]

            prospectuses = Document.objects.filter(
                company=company,
                cat__type='prospectuses'
            ).order_by('-date')[:9]

            proxies = Document.objects.filter(
                company=company,
                cat__type='proxies'
            ).order_by('-date')[:9]

            ownership = Document.objects.filter(
                company=company,
                cat__type='ownership'
            ).order_by('-date')[:9]

            others = Document.objects.filter(
                company=company,
                cat__type='other'
            ).order_by('-date')[:9]

            return render(request, 'core/company_document.html', {
                'layout': layout,
                'ticker': ticker,
                'company': company,
                'financials': financials[:8],
                'financials_count': len(financials),
                'announcements': announcements[:8],
                'announcements_count': len(announcements),
                'prospectuses': prospectuses[:8],
                'prospectuses_count': len(prospectuses),
                'proxies': proxies[:8],
                'proxies_count': len(proxies),
                'ownership': ownership[:8],
                'ownership_count': len(ownership),
                'others': others[:8],
                'others_count': len(others),
            })
        except Company.DoesNotExist:
            return render(request, 'core/company_404.html', {
                'ticker': ticker,
            })


class CompanyDocumentChrono(View):
    def get(self, request, ticker):
        try:
            if ticker.isdigit():
                company = Company.objects.get(id=ticker)
            else:
                company = Company.objects.get(ticker=ticker)

            documents = Document.objects.filter(
                company=company,
            ).order_by('-date')
            layout = company.get_layout()

            return render(request, 'core/company_document_chrono.html', {
                'layout': layout,
                'ticker': ticker,
                'company': company,
                'count': documents.count,
                'documents': documents[:20]
            })
        except Company.DoesNotExist:
            return render(request, 'core/company_404.html', {
                'ticker': ticker,
            })


class CompanyDocumentWebsite(View):
    def get(self, request, ticker):
        try:
            if ticker.isdigit():
                company = Company.objects.get(id=ticker)
            else:
                company = Company.objects.get(ticker=ticker)

            documents = WebsiteDocument.objects.filter(
                company__ticker=ticker,
            ).order_by('-last_updated')

            return render(request, 'core/company_website_document.html', {
                'ticker': ticker,
                'company': company,
                'count': documents.count,
                'documents': documents[:20]
            })
        except Company.DoesNotExist:
            return render(request, 'core/company_404.html', {
                'ticker': ticker,
            })


class CompanyDocumentSearch(View):
    def get_pagination(self, page, total_pages):

        has_prev = True if page > 1 else False
        has_next = True if page < total_pages else False
        start = max(page - 5, 1)
        end = min(page + 4, total_pages)

        pagination = []

        if has_prev:
            pagination.append({
                'label': 'Previous',
                'url': self.url + '?q={}&p={}'.format(self.query, self.page - 1),
            })

        for i in range(start, end + 1):
            pagination.append({
                'label': i,
                'url': self.url + '?q={}&p={}'.format(self.query, i),
            })

        if has_next:
            pagination.append({
                'label': 'Next',
                'url': self.url + '?q={}&p={}'.format(self.query, self.page + 1),
            })

        return pagination

    def get(self, request, ticker):
        self.url = reverse('core:company_document_search', kwargs={'ticker': ticker})
        self.query = request.GET.get('q', None)
        self.page = int(request.GET.get('p', 1))

        if not self.query:
            return HttpResponseRedirect(reverse('core:company_document', kwargs={'ticker': ticker}))

        idx_from = (self.page - 1) * 10
        idx_to = self.page * 10 - 1

        s = ESDocument.search()
        s = s.sort('-created_at').query(
            'match',
            ticker=ticker
        ).query(
            'match',
            body=self.query
        ).highlight(
            'body',
            fragment_size=150,
            number_of_fragments=5
        )
        results = s[idx_from:idx_to].execute()

        total_hits = results.hits.total
        total_pages = int(math.ceil(total_hits / 10.0))
        pages = self.get_pagination(self.page, total_pages)

        c = Company.objects.get(ticker=ticker)

        return render(request, 'core/company_document_search.html', {
            'company': c,
            'page': self.page,
            'pages': pages,
            'query': self.query,
            'results': results,
            'ticker': ticker,
            'total_hits': total_hits,
        })


class Search(View):
    def get(self, request):
        params = request.GET
        query = params['q']

        companies = Company.objects.filter(
            Q(short_name__icontains=query) | Q(ticker__startswith=query)
        )

        return render(request, 'core/search.html', {
            'query': query,
            'results': len(companies),
            'companies': companies,
        })


class Latest(View):
    def get(self, request):
        one_week_ago = datetime.now() - timedelta(days=7)

        docs = Document.objects.filter(
            cat__type='prospectuses',
            date__gte=one_week_ago,
        ).order_by('-date')

        new_issuers = docs.filter(company__ticker__isnull=True)
        existing_issuers = docs.filter(company__ticker__isnull=False)

        return render(request, 'core/latest.html', {
            'new_issuers': new_issuers,
            'existing_issuers': existing_issuers,
        })


class DocumentDetail(View):
    def get(self, request, id):
        document = Document.objects.get(id=id)
        company = Company.objects.get(id=document.company_id)

        return render(request, 'core/document.html', {
            'document': document,
            'company': company,
        })


class WebsiteDocumentDetail(View):
    def get(self, request, id):
        document = WebsiteDocument.objects.get(id=id)
        company = Company.objects.get(id=document.company_id)

        return render(request, 'core/website_document.html', {
            'document': document,
            'company': company,
        })
