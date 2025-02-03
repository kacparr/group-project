from django.shortcuts import render, redirect
from cart.cart import Cart
from payment.forms import ChangeShippingForm, PaymentForm
from payment.models import ShippingAddress, Order, OrderItem
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from store.models import Products
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
                  {"cart_products": cart_products,
                    "quantities": quantities,
                    'totals':totals, 
                    'ship_form':ship_form})

def billing_info(request):
    if not request.POST:
        messages.success(request, "Access denied.")
        return redirect('home')
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()

    my_shipping = request.POST
    request.session['my_shipping'] = my_shipping

    if request.user.is_authenticated:
            billing_form = PaymentForm()
            return render(request, "payment/billing_info.html",
                  {"cart_products": cart_products,
                    "quantities": quantities,
                    'totals':totals, 
                    'ship_info':request.POST,
                    'billing_form':billing_form})
    else:
            billing_form = PaymentForm()
            return render(request, "payment/billing_info.html",
                  {"cart_products": cart_products,
                    "quantities": quantities,
                    'totals':totals, 
                    'ship_info':request.POST,
                    'billing_form':billing_form})  
    # ship_form = request.POST
    # return render(request, "payment/billing_info.html",
    #               {"cart_products": cart_products,
    #                 "quantities": quantities,
    #                 'totals':totals, 
    #                 'ship_form':ship_form})

def process_order(request):
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()
    if not request.POST:
        messages.success(request, "Access denied.")
        return redirect('home')
    payment_form = PaymentForm(request.POST or None)   
    my_shipping = request.session.get('my_shipping')

    full_name = my_shipping['shipping_full_name']
    email = my_shipping['shipping_email']
    shipping_address = f"{my_shipping['shipping_address1']}\n{my_shipping['shipping_address2']}\n{my_shipping['shipping_city']}\n{my_shipping['shipping_area']}\n{my_shipping['shipping_zipcode']}\n{my_shipping['shipping_country']}\n"
    amount_paid = totals 
    if request.user.is_authenticated:
        user = request.user
        create_order = Order(
            user=user,
            full_name=full_name,
            email=email,
            shipping_address=shipping_address,
            amount_paid=amount_paid
        )
        create_order.save()
        order_id = create_order.pk
        for product in cart_products():
            product_id = product.id
            price = product.pk
            print(product_id)
        for k,v in quantities().items():
            if int(k) == product.id:
                    create_order_item = OrderItem(order_id=order_id,product_id=product_id,user=user,quantity=v,price=price)
                    create_order_item.save()
        for k in list(request.session.keys()):
            if k == "session_key":
                del request.session[k]
        messages.success(request, "Order placed.")
        return redirect("home")

    else:
        create_order = Order(
            full_name=full_name,
            email=email,
            shipping_address=shipping_address,
            amount_paid=amount_paid
        )
        create_order.save()
        order_id = create_order.pk
        for product in cart_products():
            product_id = product.id
            price = product.pq
        for k,v in quantities().items():
            if int(k) == product.id:
                    create_order_item = OrderItem(order_id=order_id,product_id=product_id ,quantity=v,price=price)
                    create_order_item.save()
        for k in list(request.session.keys()):
            if k == "session_key":
                del request.session[k]
        messages.success(request, "Order placed.")
        return redirect("home")
 

