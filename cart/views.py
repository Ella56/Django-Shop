from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import TemplateView,ListView,CreateView,FormView,DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from product.models import *
import uuid
from accounts.models import Profile, Address

# Create your views here.


class CartView(LoginRequiredMixin, TemplateView):
    template_name = 'cart/cart.html'


    def get(self, request, *args, **kwargs):
        cart = request.session.get('cart',{})
        if len(cart) > 0:
            total_price = sum([item['price'] * int(item['quantity']) for item in cart.values()])
            total_discount = sum([int(item['product_discount_price'] * int(item['quantity'])) for item in cart.values()])
            total_discount_price = total_price - total_discount
            request.session['total_price'] = total_price
            request.session['total_discount_price']  = total_discount_price
            request.session['payment_price'] = (request.session['total_price'] - request.session['total_discount_price'])
            request.session.modified = True
        return super().get(request, *args, **kwargs)
    
def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = self.request.session.get('cart', {})
        product_list = []
        for key, value in cart.items():
            product = get_object_or_404(Product, id=value['pid'])
            product_list.append(product)
        category_list = [product.category.name for product in product_list]
        products = Product.objects.filter(category__name__in=category_list)
        context['products'] = products
        return context
    

class AddtoCartView(TemplateView):
    def get(self, request, *args, **kwargs):
        pid = request.GET.get('pid')
        g_month = request.GET.get('g_month')
        color = (request.GET.get('color') 
                 if request.GET.get('color') != '' else 'تک رنگ')
        if not pid:
            messages.error(request, 'محصول نامعتبر است.')
            return redirect("product:products")
        
        product = get_object_or_404(Product, id=pid)
        guaranty = (get_object_or_404(Guaranty, months = g_month)
                    if g_month != '0' else 0)
        increase_price_with_guarany = ((product.price * guaranty.price_increase / 100)
                                       if guaranty != 0 else 0)
        price_with_discount = product.get_discounted_price()
        product_price = int(increase_price_with_guarany) + int(price_with_discount)
        cart = request.session.get('cart', {})

        found = False

        for key, item in cart.items():
            if type(item) == dict and item.get('pid'):
                if(
                    item['pid'] == int(pid)
                    and item['color'] == color
                    and item['guaranty'] == g_month
                ):
                    cart[key]['quantity'] += 1
                    cart[key]['final_price'] = (
                        cart[key]['quantity'] * product_price
                    )
                    found = True
                    break
        if not found:
            unique_id = str(uuid.uuid4())[:8]
            cart[unique_id] = {
                'pid': product.id,
                'title': product.name,
                'image' : product.img1.url if product.img1 else None,
                'price' : product.price,
                'final_price': product_price,
                'quantity' : 1,
                'guaranty' : g_month,
                'color' : color,
                'product_discount' : int(product.discount_price),
                'product_discount_price' : int(price_with_discount)
            }
        request.session['cart'] = cart
        request.session.modified = True
        messages.success(request, 'محصول به سبد خرید شما اضافه شد')
        return redirect("product:product-detail", pk=pid)
        


        
class UpdateCartView(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        messages.error(request, 'درخواست نا مناسب')
        return redirect("cart:cart")
    
    def post(self, request, *args,**kwargs):
        cart = request.session.get('cart', {})

        for uid_post, quantity_post in request.POST.items():
            for uuid in cart.keys():
                if uid_post == uuid:
                    cart[uuid]['quantity'] = quantity_post
                    product = get_object_or_404(Product, id=cart[uuid]['pid'])
                    guaranty = (get_object_or_404(Guaranty, mounts=cart[uuid]['guaranty'])
                        if cart[uuid]['guaranty'] != '0'
                        else 0
                    )
                    increase_price_with_guaranty = ((product.price * guaranty.price_increase / 100)
                                                    if guaranty != 0 else 0)
                    price_with_discount = product.get_discounted_price()
                    product_price = increase_price_with_guaranty + int(price_with_discount)
                    cart[uuid]['final_price'] = (int(cart[uuid]['guaranty']) * product_price)
                    break
        request.session['cart'] = cart
        total_price = sum([item['price'] * int(item['quantity']) for item in cart.values()])
        total_discount = sum([int(item['product_discount_price'] * int(item['quantity'])) for item in cart.values()])
        total_discount_price = total_price - total_discount
        request.session['total_price'] = total_price
        request.session['total_discoun_price'] = total_discount_price
        request.session['payment_price'] = ( request.session['total_price'] - request.session['total_discount_price'])
        request.session.modified = True
        messages.success(request, 'سبد خرید شما با موفقیت بروزرسانی شد')
        return redirect("cart:cart")
    

class DeleteCartItemView(LoginRequiredMixin, TemplateView):
    def get(self, request, *atgs, **kwargs):
        uid = kwargs.get('uid')
        cart = request.session.get('cart',{})
        if uid in cart:
            del cart[uid]
            request.session['cart'] = cart
            request.session.modified = True
            if len(cart) == 0:
                request.session['total_price'] = 0
                request.session['total_discount_price'] = 0
                request.session['payment_price'] = 0
                request.session['payment_price'] = 0
            messages.success(request, 'محصول از سبد خرید شما حذف شد')
        else:
            messages.error(request, 'محصول در سبد خرید شما وجود ندارد')
        return redirect("cart:cart")
    
    def post(self, request, *args, **kwargs):
        messages.error(request, 'درخواست نا مناسب')
        return redirect("cart:cart")
    

class CleanCartItemView(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        request.session['cart'] = {}
        request.session['total_price'] = 0
        request.session['total_discount_price'] = 0
        request.session['payment_price'] = 0
        request.session.modified = True
        messages.success(request, 'سبد خرید شما خالی شد')
        return redirect("cart:cart")
    
    
    def post(self, request, *args, **kwargs):
        messages.error(request, 'درخواست نا مناسب')
        return redirect("cart:cart")
        


class CheckoutView(LoginRequiredMixin, TemplateView):
    template_name = 'cart/checkout.html'


    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = get_object_or_404(Profile,user=self.request.user)
        try:
            address = Address.objects.filter(profile =profile).order_by('-created_at')[0]
        except:
            address = None
        context['address'] = address
        return context