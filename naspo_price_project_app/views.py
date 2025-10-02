from django.shortcuts import render
from .models import NaspoInformation
from django.db.models import Q
from django.core.paginator import Paginator
from django.db.models.expressions import RawSQL
from prometheus_client import Counter

URL_HOMEPAGE_PARAMETERS_TOTAL = Counter('Homepage_URL_Parameters_Total', 'Total URL Parameters', ['parameter'])


def homepage(request):
    # Perform searching
    request_vendor_name = request.GET.get('vendor_name', '')
    request_naspo_price = request.GET.get('naspo_price', '')
    request_list_price = request.GET.get('list_price', '')
    request_description = request.GET.get('description', '')
    request_manufacturer_part_number = request.GET.get('manufacturer_part_number', '')

    sort_value = request.GET.get('sort_value', '')
    sort_direction = request.GET.get('sort_direction', '')
    order_by = ['vendor_name','description','manufacturer_part_number']


    # Acceptable sort values
    acceptable_sort_values = ['vendor_name', 'naspo_price', 'list_price', 'description', 'manufacturer_part_number']

    if sort_value in acceptable_sort_values:
        if sort_value in ['naspo_price', 'list_price']:
            sort_value = f'{sort_value}_numeric'
        if sort_direction == 'asc':
            order_by = [sort_value]
        else:
            order_by = [f'-{sort_value}']

    query = Q()
    if request_vendor_name:
        query &= Q(vendor_name__startswith=request_vendor_name)
    if request_naspo_price:
        request_naspo_price = request_naspo_price.replace('$', '').replace(',', '')
        query &= Q(naspo_price_numeric=request_naspo_price)
    if request_list_price:
        request_list_price = request_list_price.replace('$', '').replace(',', '')
        query &= Q(list_price_numeric=request_list_price)
    if request_description:
        query &= Q(description__startswith=request_description)
    if request_manufacturer_part_number:
        query &= Q(manufacturer_part_number__startswith=request_manufacturer_part_number)

    naspo_items = NaspoInformation.objects.annotate(
        list_price_numeric=RawSQL('list_price::numeric', []),
        naspo_price_numeric=RawSQL('naspo_price::numeric', []),
    ).filter(query).order_by(*order_by)
    paginator = Paginator(naspo_items, 30)  # Show 30 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'home.html', {'naspo_items': page_obj, 'request': request})

class PrometheusEndpointMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        for param in request.GET.keys():
            URL_HOMEPAGE_PARAMETERS_TOTAL.labels(parameter=param).inc()

        return response