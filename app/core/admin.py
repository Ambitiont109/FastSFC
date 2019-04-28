from django.contrib import admin
from app.core.models import *
from django.utils.translation import ugettext_lazy as _
from django.db.models import F


class PeriodAdmin(admin.ModelAdmin):
    list_display = ["short_name"]


class DocumentCategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "description"]


class DocumentSubcategoryAdmin(admin.ModelAdmin):
    list_display = ["name"]


class ExchangeAdmin(admin.ModelAdmin):
    list_display = ["short_name", "full_name"]


class CompanyAdmin(admin.ModelAdmin):
    list_display = ["ticker", "full_name", "short_name", "website_url", "exchange", "last_updated"]
    search_fields = ["full_name"]


class DocumentAdmin(admin.ModelAdmin):
    list_display = ["company", "date", "document_url", "cat", "subcat", "description", "size", "filetype"]
    search_fields = ["company__ticker", "company__full_name"]

# DocumentCount - Filter
# Selects tickers that have an complete/incomplete set of filings (i.e. our_count < actual_count)
# https://docs.djangoproject.com/en/dev/ref/contrib/admin/


class IncompleteFilingFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _('complete / incomplete filings')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'filter_tickers'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('complete', _('Complete')),
            ('incomplete', _('Incomplete')),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        if self.value() == 'complete':
            return queryset.filter(actual_count=F('our_count'))
        elif self.value() == 'incomplete':
            return queryset.exclude(actual_count=F('our_count'))

# DocumentCount - Action
# Updates internal document count


def refresh_document_count(modeladmin, request, queryset):
    for obj in queryset:
        count = Document.objects.filter(company__ticker=obj.company.ticker).count()
        obj.our_count = count
        obj.save()


class DocumentCountAdmin (admin.ModelAdmin):
    list_display = ["company", "actual_count", "our_count"]
    list_filter = (IncompleteFilingFilter,)
    actions = [refresh_document_count]


admin.site.register(Period, PeriodAdmin)
admin.site.register(DocumentCategory, DocumentCategoryAdmin)
admin.site.register(DocumentSubcategory, DocumentSubcategoryAdmin)
admin.site.register(Exchange, ExchangeAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(Document, DocumentAdmin)
admin.site.register(DocumentCount, DocumentCountAdmin)
