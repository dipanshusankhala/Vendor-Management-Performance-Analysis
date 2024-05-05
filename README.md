# Vendor Management System with Performance Metrics
Implemented a Vendor Management System using Django and Django REST Framework. This
system will handle vendor profiles, track purchase orders, and calculate vendor performance
metrics. This System will calculate the Realtime Performance of each Vendor using the vendor Code . 

## Core Features

There are 3 App in the Django Project named VendorProfile,PurchaseOrder,HistoricalPerformance which stores the information about vendor & purchase order and Provide tthe data integrity
using Foreign Key.<br>

1. Vendor Profile Management:<br>
API Endpoints:<br>
● POST /api/vendors/   :- Create a new vendor.<br>
● GET /api/vendors/   :- List all vendors.<br>
● GET /api/vendors/{vendor_id}/   :- Retrieve a specific vendor's details.<br>
● PUT /api/vendors/{vendor_id}/   :- Update a vendor's details.<br>
● DELETE /api/vendors/{vendor_id}/    :- Delete a vendor.<br>


2. Purchase Order Tracking:<br>
API Endpoints:<br>
● POST /api/purchase_orders/: Create a purchase order.<br>
● GET /api/purchase_orders/: List all purchase orders with an option to filter by
vendor.<br>
● GET /api/purchase_orders/{po_id}/: Retrieve details of a specific purchase order.<br>
● PUT /api/purchase_orders/{po_id}/: Update a purchase order.<br>
● DELETE /api/purchase_orders/{po_id}/: Delete a purchase order.<br>




3. Vendor Performance Evaluation:<br>
Metrics:<br>
● On-Time Delivery Rate: Percentage of orders delivered by the promised date.<br>
● Quality Rating: Average of quality ratings given to a vendor’s purchase orders.<br>
● Response Time: Average time taken by a vendor to acknowledge or respond to
purchase orders.<br>
● Fulfilment Rate: Percentage of purchase orders fulfilled without issues.<br>
API Endpoints:<br>
● GET /api/vendors/{vendor_id}/performance: Retrieve a vendor's performance
metrics.<br>


## Backend Logic for Performance Metrics

These Metric calculate the Performance of the Particular Vendor using the Vendor code <br>

On-Time Delivery Rate:<br>
● Calculated each time a PO status changes to 'completed'.<br>
● Logic: Count the number of completed POs delivered on or before<br>
delivery_date and divide by the total number of completed POs for that vendor.

Quality Rating Average:<br>
● Updated upon the completion of each PO where a quality_rating is provided.<br>
● Logic: Calculate the average of all quality_rating values for completed POs of
the vendor.<br>

Average Response Time:<br>
● Calculated each time a PO is acknowledged by the vendor.<br>
● Logic: Compute the time difference between issue_date and
acknowledgment_date for each PO, and then find the average of these times
for all POs of the vendor.<br>

Fulfilment Rate:<br>
● Calculated upon any change in PO status.<br>
● Logic: Divide the number of successfully fulfilled POs (status 'completed'
without issues) by the total number of POs issued to the vendor.<br>



