from django.db.models import Avg, Count, F
from django.http import JsonResponse
from django.utils import timezone
from Vendor_profile.models import Vendor
from PurchaseOrder.models import PurchaseOrder
import logging
from django.db.models import Q


def calculate_on_time_delivery_rate(vendor):
    completed_pos = PurchaseOrder.objects.filter(
        vendor=vendor,
        status='completed'
    )
    completed_pos_count = completed_pos.count()
    print(f"Count of Completed Purchase Orders: {completed_pos_count}")
    total_completed_pos_count = 0
    completed_on_time_count = 0
    for po in completed_pos:
        total_completed_pos_count += 1
        if po.delivery_date <= po.acknowledgment_date:
            completed_on_time_count += 1
    #on-time delivery rate
    # converted into Percentage
    if total_completed_pos_count > 0:
        return (completed_on_time_count / total_completed_pos_count)*100
    else:
        return 0


def calculate_quality_rating_avg(vendor):
    completed_pos_with_rating = PurchaseOrder.objects.filter(vendor=vendor, status='completed', quality_rating__isnull=False)
    return completed_pos_with_rating.aggregate(avg_quality_rating=Avg('quality_rating'))['avg_quality_rating'] or 0

def calculate_average_response_time(vendor):
    completed_pos_with_acknowledgment = PurchaseOrder.objects.filter(vendor=vendor, status='completed', acknowledgment_date__isnull=False)
    response_times = [(po.acknowledgment_date - po.issue_date).total_seconds() for po in completed_pos_with_acknowledgment]
    return (sum(response_times) / len(response_times))/3600 if response_times else 0

def calculate_fulfillment_rate(vendor):
    total_pos = PurchaseOrder.objects.filter(vendor=vendor)
    total_pos_count = total_pos.count()
    print(f"Total Purchase Orders: {total_pos_count}")
    fulfilled_pos_count = total_pos.filter(status='completed').count()
    return (fulfilled_pos_count / total_pos_count)*100 if total_pos_count > 0 else 0

def get_vendor_performance(request, vendor_code):
    try:
        vendor = Vendor.objects.get(vendor_code=vendor_code)
    except Vendor.DoesNotExist:
        return JsonResponse({'error': 'Vendor does not exist'}, status=404)
    
    performance_data = {
        'on_time_delivery_rate': calculate_on_time_delivery_rate(vendor),
        'quality_rating_avg': calculate_quality_rating_avg(vendor),
        'average_response_time': calculate_average_response_time(vendor),
        'fulfillment_rate': calculate_fulfillment_rate(vendor)
    }
    return JsonResponse(performance_data)

def acknowledge_purchase_order(request, po_number):
    try:
        po = PurchaseOrder.objects.get(po_number=po_number)
    except PurchaseOrder.DoesNotExist:
        return JsonResponse({'error': 'Purchase Order does not exist'}, status=404)
    
    if request.method == 'POST':
        acknowledgment_date = timezone.now()
        po.acknowledgment_date = acknowledgment_date
        po.save()
        # Recalculate average response time
        vendor = po.vendor
        avg_response_time = calculate_average_response_time(vendor)
        # Update Historical Performance Model
        HistoricalPerformanceModel.objects.create(
            vendor=vendor,
            date=acknowledgment_date,
            average_response_time=avg_response_time
        )

        return JsonResponse({'message': 'Purchase Order acknowledged successfully'})
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
