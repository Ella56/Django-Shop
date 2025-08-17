from django.shortcuts import render
from django.views.generic import TemplateView, CreateView
from .forms import ContactForm
from django.contrib import messages
from product.models import Product, SpecialOffer
from django.utils import timezone
from blog.models import Blog

# Create your views here.



class HomeView(TemplateView):
    template_name = 'root/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['selected_products'] = Product.objects.all().order_by('-total_favorites')[:4]
        context['discounted_products'] = Product.objects.filter(discount_price__gt=0).order_by('-discount_price')[:100]
        context['popular_products'] = Product.objects.all().order_by('-total_views')[:12]
        special_offers = SpecialOffer.objects.filter(start_date__lte=timezone.now(), end_date__gte=timezone.now()
        ).order_by("-product__discount_price")
        context['blogs'] = Blog.objects.filter(status=True).order_by('-created_at')[:3]
        context['special_offers'] = special_offers
        context["best_selling_products"] = Product.objects.all().order_by("-total_sold")[:12]
        special_offers_list = list(special_offers)
        for offer in special_offers_list:
           offer.remaining = offer.remaining_time()

        context["special_offers"] = special_offers_list
        return context




class ContactView(CreateView):
    template_name = 'root/contact.html'
    form_class = ContactForm
    success_url = '/contact/'


    def form_valid(self, form):
        # form.save()
        messages.success(self.request,'پیام شما با موفقیت دریافت شد . بزودی با شما تماس خواهیم گرفت')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'خطا در ارسال اطلاعات . لطفا دوباره تلاش کنید')
        return super().form_invalid(form)



class AboutView(TemplateView):
    template_name = 'root/about.html'


class FaqView(TemplateView):
    template_name = 'root/faq.html'