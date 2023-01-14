from .models import *
def place_order(order):
    crew=DeliveryProfile.objects.filter(availability_status=True).first()
    if crew!=None:
        crew.orders=order
        return True
    else:
        orders_places.objects.create(order=order)
        return False
    
