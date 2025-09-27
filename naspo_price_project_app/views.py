from django.shortcuts import render
from .models import NaspoInformation
from django.db.models import Q
from django.core.paginator import Paginator
from django.db.models.expressions import RawSQL

def homepage(request):

    # Perform searching
    request_vendor_name = request.GET.get('vendor_name', '')
    request_naspo_price = request.GET.get('naspo_price', '')
    request_list_price = request.GET.get('list_price', '')
    request_description = request.GET.get('description', '')
    request_manufacturer_part_number = request.GET.get('manufacturer_part_number', '')

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
    ).filter(query).order_by('vendor_name','description','manufacturer_part_number')
    paginator = Paginator(naspo_items, 30)  # Show 30 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'home.html', {'naspo_items': page_obj, 'request': request})