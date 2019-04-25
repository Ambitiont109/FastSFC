import django_filters
from django.contrib.auth.models import User
from app.core.models import Company, Exchange, Document, WebsiteDocument, DocumentCategory, DocumentSubcategory, Price, UserProfile, Watchlist
from app.core.api.shared import *
from rest_framework import routers, serializers, views, viewsets, filters, pagination
from rest_framework.response import Response
from rest_framework.decorators import api_view


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'is_staff')


class ExchangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exchange
        fields = ('short_name', 'full_name')


class DocumentCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentCategory
        fields = ('name', 'type')


class DocumentSubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentSubcategory
        fields = ('name')


class CompanySerializer(serializers.ModelSerializer):
    exchange = serializers.StringRelatedField()

    class Meta:
        model = Company
        fields = ('ticker', 'full_name', 'short_name', 'exchange', 'website')


class WatchlistSerializer(serializers.ModelSerializer):
    meta = JSONSerializerField()
    company = CompanySerializer()
    user = UserSerializer()

    class Meta:
        model = Watchlist
        fields = ('id', 'company', 'user', 'meta')


class DocumentSerializer(serializers.ModelSerializer):
    company = CompanySerializer()
    cat = DocumentCategorySerializer()
    subcat = serializers.StringRelatedField()

    class Meta:
        model = Document
        fields = ('id', 'company', 'cat', 'subcat', 'date', 'description', 'filetype', 'size', 'url', 'last_updated')


class WebsiteDocumentSerializer(serializers.ModelSerializer):
    company = CompanySerializer()

    class Meta:
        model = WebsiteDocument
        fields = ('id', 'company', 'description', 'url', 'last_updated')


class PriceSerializer(serializers.ModelSerializer):
    company = serializers.StringRelatedField()

    class Meta:
        model = Price
        fields = ('company', 'date', 'open', 'close', 'high', 'low', 'adj_close', 'volume')

# Filters


class PriceFilter(django_filters.FilterSet):
    ticker = django_filters.CharFilter(name='company__ticker')
    date_from = django_filters.DateFilter(name='date', lookup_type='gte')

    class Meta:
        model = Price
        fields = ('company', 'date', 'open', 'close', 'high', 'low', 'adj_close', 'volume')


class DocumentFilter(django_filters.FilterSet):
    ticker = django_filters.CharFilter(name='company__ticker')
    type = django_filters.CharFilter(name='cat__type')
    date_from = django_filters.DateFilter(name='date', lookup_type='gte')

    class Meta:
        model = Document
        fields = ('ticker', 'cat', 'subcat', 'date', 'description', 'filetype', 'size', 'url', 'last_updated')


class WebsiteDocumentFilter(django_filters.FilterSet):
    ticker = django_filters.CharFilter(name='company__ticker')
    type = django_filters.CharFilter(name='cat__type')

    class Meta:
        model = WebsiteDocument
        fields = ('ticker', 'description', 'url', 'last_updated')

# Pagination


class PricePagination(pagination.LimitOffsetPagination):
    default_limit = 251
    max_limit = 1000

# ViewSets


class WatchlistViewSet(viewsets.ModelViewSet):
    serializer_class = WatchlistSerializer

    def get_queryset(self):
        user = self.request.user
        return Watchlist.objects.filter(user=user)



class ExchangeViewSet(viewsets.ModelViewSet):
    queryset = Exchange.objects.all()
    serializer_class = ExchangeSerializer


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

    filter_backends = (
        filters.DjangoFilterBackend,
        filters.OrderingFilter,
    )
    filter_class = DocumentFilter
    ordering_fields = ('date')
    ordering = ('-date',)


class WebsiteDocumentViewSet(viewsets.ModelViewSet):
    queryset = WebsiteDocument.objects.all()
    serializer_class = WebsiteDocumentSerializer

    filter_backends = (
        filters.DjangoFilterBackend,
        filters.OrderingFilter,
    )
    filter_class = WebsiteDocumentFilter
    ordering_fields = ('last_updated')
    ordering = ('-last_updated',)


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

    filter_backends = (filters.SearchFilter,)
    search_fields = ('ticker', 'short_name')


class PriceViewSet(viewsets.ModelViewSet):
    queryset = Price.objects.all()
    serializer_class = PriceSerializer
    pagination_class = PricePagination

    filter_backends = (
        filters.DjangoFilterBackend,
        filters.OrderingFilter,
    )
    filter_class = PriceFilter
    ordering_fields = ('date')
    ordering = ('-date',)


router = routers.DefaultRouter()
router.register('exchange', ExchangeViewSet)
router.register('document', DocumentViewSet)
router.register('website-document', WebsiteDocumentViewSet)
router.register('company', CompanyViewSet)
router.register('price', PriceViewSet)
router.register('metric', MetricViewSet)
router.register('timeseries', TimeseriesViewSet)
router.register('watchlist', WatchlistViewSet, base_name='watchlist')
