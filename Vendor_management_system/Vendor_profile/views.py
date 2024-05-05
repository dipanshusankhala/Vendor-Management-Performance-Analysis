from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Vendor
import json

# Create a new vendor
@csrf_exempt
def create_vendor(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('name')
        contact_details = data.get('contact_details')
        address = data.get('address')
        vendor_code = data.get('vendor_code')
        on_time_delivery_rate = data.get('on_time_delivery_rate', 0.0)
        quality_rating_avg = data.get('quality_rating_avg', 0.0)
        average_response_time = data.get('average_response_time', 0.0)
        fulfillment_rate = data.get('fulfillment_rate', 0.0)
        
        # Check if vendor with provided vendor_code already exists
        if Vendor.objects.filter(vendor_code=vendor_code).exists():
            return JsonResponse({'error': 'Vendor with this vendor_code already exists'}, status=400)
        
        # Create new vendor
        vendor = Vendor(name=name, contact_details=contact_details, address=address, vendor_code=vendor_code,
                        on_time_delivery_rate=on_time_delivery_rate, quality_rating_avg=quality_rating_avg,
                        average_response_time=average_response_time, fulfillment_rate=fulfillment_rate)
        vendor.save()
        
        return JsonResponse({'message': 'Vendor created successfully'}, status=201)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)

# List all vendors
@csrf_exempt
def list_vendors(request):
    if request.method == 'GET':
        vendors = Vendor.objects.all()
        data = [{'id': vendor.id, 'name': vendor.name, 'contact_details': vendor.contact_details,
                 'address': vendor.address, 'vendor_code': vendor.vendor_code,
                 'on_time_delivery_rate': vendor.on_time_delivery_rate,
                 'quality_rating_avg': vendor.quality_rating_avg,
                 'average_response_time': vendor.average_response_time,
                 'fulfillment_rate': vendor.fulfillment_rate} for vendor in vendors]
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'error': 'Only GET requests are allowed'}, status=405)


# Retrieve a specific vendor's details
def get_vendor(request, vendor_code):
    if request.method == 'GET':
        try:
            vendor = Vendor.objects.get(vendor_code=vendor_code)
            data = {'id': vendor.id, 'name': vendor.name, 'contact_details': vendor.contact_details,
                    'address': vendor.address, 'vendor_code': vendor.vendor_code,
                    'on_time_delivery_rate': vendor.on_time_delivery_rate,
                    'quality_rating_avg': vendor.quality_rating_avg,
                    'average_response_time': vendor.average_response_time,
                    'fulfillment_rate': vendor.fulfillment_rate}
            return JsonResponse(data)
        except Vendor.DoesNotExist:
            return JsonResponse({'error': 'Vendor does not exist'}, status=404)
    else:
        return JsonResponse({'error': 'Only GET requests are allowed'}, status=405)

# Update a vendor's details
@csrf_exempt
def update_vendor(request, vendor_code):
    try:
        vendor = Vendor.objects.get(vendor_code=vendor_code)
    except Vendor.DoesNotExist:
        return JsonResponse({'error': 'Vendor does not exist'}, status=404)
    
    if request.method == 'PUT':
        data = json.loads(request.body)
        vendor.name = data.get('name', vendor.name)
        vendor.contact_details = data.get('contact_details', vendor.contact_details)
        vendor.address = data.get('address', vendor.address)
        vendor.on_time_delivery_rate = data.get('on_time_delivery_rate', vendor.on_time_delivery_rate)
        vendor.quality_rating_avg = data.get('quality_rating_avg', vendor.quality_rating_avg)
        vendor.average_response_time = data.get('average_response_time', vendor.average_response_time)
        vendor.fulfillment_rate = data.get('fulfillment_rate', vendor.fulfillment_rate)
        vendor.save()
        return JsonResponse({'message': 'Vendor updated successfully'})
    else:
        return JsonResponse({'error': 'Only PUT requests are allowed'}, status=405)
# Delete a vendor
@csrf_exempt
def delete_vendor(request, vendor_code):
    try:
        vendor = Vendor.objects.get(vendor_code=vendor_code)
    except Vendor.DoesNotExist:
        return JsonResponse({'error': 'Vendor does not exist'}, status=404)
    
    if request.method == 'DELETE':
        vendor.delete()
        return JsonResponse({'message': 'Vendor deleted successfully'})
    else:
        return JsonResponse({'error': 'Only DELETE requests are allowed'}, status=405)