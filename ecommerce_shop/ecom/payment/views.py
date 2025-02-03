from django.shortcuts import render
from cart.cart import Cart
from payment.forms import ChangeShippingForm
from payment.models import ShippingAddress
# Create your views here.
def payment_success(request):
    return render(request, "payment/payment_success.html")

def checkout(request):
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()

    if not request.user.is_authenticated:
            ship_form = ChangeShippingForm(request.POST or None)
    else:
            try:
                shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
            except ShippingAddress.DoesNotExist:
                shipping_user = None
            ship_form = ChangeShippingForm(request.POST or None,instance=shipping_user)

    return render(request, "payment/checkout.html",
                  {"cart_products": cart_products, "quantities": quantities, 'totals':totals, 'ship_form':ship_form})
