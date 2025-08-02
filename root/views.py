from django.shortcuts import render
from django.views.generic import TemplateView, CreateView
from .forms import ContactForm
from django.contrib import messages

# Create your views here.



class HomeView(TemplateView):
    template_name = 'root/index.html'



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