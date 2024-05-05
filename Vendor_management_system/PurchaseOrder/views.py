from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import PurchaseOrder
from Vendor_profile.models import Vendor
import json
from django.utils import timezone
import datetime

@csrf_exempt
def create_purchase_order(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            vendor = Vendor.objects.get(vendor_code=data['vendor_code'])
            po = PurchaseOrder.objects.create(
                po_number=data['po_number'],
                vendor=vendor,
                order_date=timezone.make_aware(datetime.datetime.strptime(data['order_date'], '%Y-%m-%dT%H:%M:%S')),
                delivery_date=timezone.make_aware(datetime.datetime.strptime(data.get('delivery_date'), '%Y-%m-%dT%H:%M:%S')) if data.get('delivery_date') else None,
                items=data['items'],
                quantity=data['quantity'],
                status=data['status'],
                quality_rating=data.get('quality_rating'),
                acknowledgment_date=timezone.make_aware(datetime.datetime.strptime(data.get('acknowledgment_date'), '%Y-%m-%dT%H:%M:%S')) if data.get('acknowledgment_date') else None,
                issue_date=timezone.make_aware(datetime.datetime.strptime(data.get('issue_date'), '%Y-%m-%dT%H:%M:%S')) if data.get('issue_date') else None
            )
            return JsonResponse({'message': 'Purchase Order created successfully'}, status=201)
        except KeyError:
            return JsonResponse({'error': 'Incomplete data provided'}, status=400)
        except Vendor.DoesNotExist:
            return JsonResponse({'error': 'Vendor with provided vendor_code does not exist'}, status=400)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)


def list_purchase_orders(request):
    if request.method == 'GET':
        purchase_orders = PurchaseOrder.objects.all()
        data = [{'po_number': po.po_number, 'vendor': po.vendor.vendor_code, 'order_date': po.order_date,
                 'delivery_date': po.delivery_date, 'items': po.items, 'quantity': po.quantity,
                 'status': po.status, 'quality_rating': po.quality_rating,
                 'issue_date': po.issue_date, 'acknowledgment_date': po.acknowledgment_date} for po in purchase_orders]
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'error': 'Only GET requests are allowed'}, status=405)

def get_purchase_order(request, po_number):
    if request.method == 'GET':
        try:
            po = PurchaseOrder.objects.get(po_number=po_number)
            data = {'po_number': po.po_number, 'vendor': po.vendor.vendor_code, 'order_date': po.order_date,
                    'delivery_date': po.delivery_date, 'items': po.items, 'quantity': po.quantity,
                    'status': po.status, 'quality_rating': po.quality_rating,
                    'issue_date': po.issue_date, 'acknowledgment_date': po.acknowledgment_date}
            return JsonResponse(data)
        except PurchaseOrder.DoesNotExist:
            return JsonResponse({'error': 'Purchase Order does not exist'}, status=404)
    else:
        return JsonResponse({'error': 'Only GET requests are allowed'}, status=405)

@csrf_exempt
def update_purchase_order(request, po_number):
    try:
        po = PurchaseOrder.objects.get(po_number=po_number)
    except PurchaseOrder.DoesNotExist:
        return JsonResponse({'error': 'Purchase Order does not exist'}, status=404)
    
    if request.method == 'PUT':
        data = json.loads(request.body)
        try:
            vendor = Vendor.objects.get(vendor_code=data['vendor_code'])
            po.vendor = vendor
        except Vendor.DoesNotExist:
            return JsonResponse({'error': 'Vendor with provided vendor_code does not exist'}, status=400)
        po.order_date = data.get('order_date', po.order_date)
        po.delivery_date = data.get('delivery_date', po.delivery_date)
        po.items = data.get('items', po.items)
        po.quantity = data.get('quantity', po.quantity)
        po.status = data.get('status', po.status)
        po.quality_rating = data.get('quality_rating', po.quality_rating)
        po.acknowledgment_date = data.get('acknowledgment_date', po.acknowledgment_date)
        po.issue_date = timezone.make_aware(datetime.datetime.strptime(data.get('issue_date'), '%Y-%m-%dT%H:%M:%S')) if data.get('issue_date') else po.issue_date
        po.save()
        return JsonResponse({'message': 'Purchase Order updated successfully'})
    else:
        return JsonResponse({'error': 'Only PUT requests are allowed'}, status=405)

@csrf_exempt
def delete_purchase_order(request, po_number):
    try:
        po = PurchaseOrder.objects.get(po_number=po_number)
    except PurchaseOrder.DoesNotExist:
        return JsonResponse({'error': 'Purchase Order does not exist'}, status=404)
    
    if request.method == 'DELETE':
        po.delete()
        return JsonResponse({'message': 'Purchase Order deleted successfully'})
    else:
        return JsonResponse({'error': 'Only DELETE requests are allowed'}, status=405)












