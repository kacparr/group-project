from store.models import Products, Profile
class Cart():
    def __init__(self, request):
        self.session = request.session

        self.request = request
        cart = self.session.get('session_key')

        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}


        self.cart = cart

    def add(self, product, quantity):
        product_id = str(product.id)
        product_qty = str(quantity)
        if product.id in self.cart:
            pass
        else:
            self.cart[product_id] = int(product_qty)

        self.session.modified = True

        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            carti = str(self.cart)
            carti = carti.replace("\'","\"")
            current_user.update(old_cart=str(carti))

    def db_add(self, product, quantity):
        product_id = str(product)
        product_qty = str(quantity)
        if product_id in self.cart:
            pass
        else:
            self.cart[product_id] = int(product_qty)

        self.session.modified = True

        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            carti = str(self.cart)
            carti = carti.replace("\'","\"")
            current_user.update(old_cart=str(carti))
    def __len__(self):
        return len(self.cart)

    def get_prods(self):
        product_ids = self.cart.keys()
        products = Products.objects.filter(id__in=product_ids)

        return products

    def get_quants(self):
        quantities = self.cart
        return quantities

    def cart_total(self):
        product_ids = self.cart.keys()
        products = Products.objects.filter(id__in=product_ids)
        quantites = self.cart
        total = 0
        for k,v in quantites.items():
            k = int(k)
            for product in products:
                if product.id == k:
                    total += (product.price * v)
        return total

    def update(self, product, quantity):
        product_id = str(product)
        product_qty = int(quantity)

        # Get cart
        ourcart = self.cart
        # Update Dictionary/cart
        ourcart[product_id] = product_qty

        self.session.modified = True

        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            carti = str(self.cart)
            carti = carti.replace("\'","\"")
            current_user.update(old_cart=str(carti))
        thing =self.cart
        return thing

    def delete(self, product):
        product_id = str(product)
        # Delete from dictionary/cart
        if product_id in self.cart:
            del self.cart[product_id]

        self.session.modified = True
        
        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            carti = str(self.cart)
            carti = carti.replace("\'","\"")
            current_user.update(old_cart=str(carti))

