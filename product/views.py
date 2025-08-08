from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView
from .models import Product, Comment
from .forms import CommentFrom,RepliesForm
from django.contrib import messages
from accounts.models import Profile
from django.db.models import Q

# Create your views here.


class ProductView(ListView):
    model = Product
    template_name = 'product/products.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["last_products"] = self.model.objects.all().order_by('-created_at')[:3]
        context["product_count"] = self.model.objects.all().count()
        return context



class ProductListView(ListView):
    model = Product
    template_name = "product/products-list.html"
    context_object_name = "products"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["last_products"] = self.model.objects.all().order_by('-created_at')[:3]
        context["product_count"] = self.model.objects.all().count()
        return context
    


    def get_queryset(self):
        if self.request.GET.get('search'):
            return Product.objects.filter(name__contains = self.request.GET.get('serach'))
        categories = self.request.GET.getlist('category')
        category_detail = self.request.GET.get('detail-category')
        if categories:
            query = Q()
            for category in categories:
                query |= Q(category__id=category)
                query |= Q(category__parent__id=category)
                query |= Q(category__parent__parent__id=category)
            
            
            return Product.objects.filter(query)
        
        if category_detail:
            return Product.objects.filter(category__name=category_detail)
        

        max_price = self.request.GET.get('max-price')
        min_price = self.request.GET.get('min-price')

        if min_price and max_price:
            try:
                min_price = int(min_price)
                max_price = int(max_price)
                return Product.objects.filter(price__gte=min_price,price__lte=max_price)
            except ValueError:
                pass

        guaranty = self.request.GET.get('guaranty')
        if guaranty == "true":
            return Product.objects.filter(has__guaranty=True)
        

        return Product.objects.all()



class ProductDetailView(DetailView):
    model = Product
    template_name = "product/product.html"
    context_object_name = 'product'


    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.total_views += 1
        self.object.save()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.object.category.name
        context['related_products'] = self.model.objects.filter(category__name = category).order_by("created_at")[:30]
        return context
    





class ProductCommentView(CreateView):
    form_class = CommentFrom

    def get(self, request, *args, **kwargs):
        product = get_object_or_404(Product,pk = kwargs['pk'])
        return redirect(f'products/product-detail/{product.pk}')

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(self.request,"لطفاً وارد شوید")
            return redirect("accounts:login")
        product = get_object_or_404(Product,pk=kwargs["pk"])
        user = request.user
        email = user.email
        profile = Profile.objects.get(user=user)
        form = self.get_form()
        if form.is_valid():
            comment = form.save(commit=False)
            comment.product = product
            comment.name = profile
            comment.email = email
            comment.save()
            messages.success(request,  'کامنت شما دریافت شد . در صورت تایید مدیر سایت نمایش داده می شود')
            return redirect('product:product-detail', pk=product.pk)
        else:
            return self.form_invalid(form)
        

    def form_invalid(self, form):
        messages.error(self.request, 'خطا در ارسال کامنت')
        return super().form_invalid(form)
    




class ProductReplyView(CreateView):
    form_class = RepliesForm


    def get(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=kwargs['pk'])
        product = comment.product
        return redirect(f'products/product-detail/{product.pk}')
    
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(self.request,"لطفاً وارد شوید")
            return redirect('accounts:login')
        comment = get_object_or_404(Comment, pk=kwargs['pk'])
        user = request.user
        email = user.email
        profile = Profile.objects.get(user=user)
        form = self.get_form()
        if form.is_valid():
            reply = form.save(commit=False)
            reply.comment = Comment
            reply.name = profile
            reply.email = email
            reply.save()
            messages.success(request, 'پاسخ شما دریافت شد . در صورت تایید مدیر سایت نمایش داده می شود')
            return redirect('product:product-detail', pk=comment.product.pk)
        else:
            return self.form_invalid(form)
        

    def form_invalid(self, form):
        messages.error(self.request, 'خطا در ارسال پاسخ')
        return super().form_invalid(form)