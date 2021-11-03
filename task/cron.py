from products.models import Product
import datetime

def clear_expired():
    Product.objects.filter(expiry_date_lt=datetime.datetime.now().date()).delete()