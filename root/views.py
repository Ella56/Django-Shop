from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.



class HomeView(TemplateView):
    template_name = 'root/index.html'



class ContactView(TemplateView):
    template_name = 'root/contact.html'



class AboutView(TemplateView):
    template_name = 'root/about.html'