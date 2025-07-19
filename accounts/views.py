from django.shortcuts import render, redirect
from django.views.generic import FormView,CreateView, TemplateView, UpdateView
from .forms import LoginForm, SignupForm, EditProfileForm
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import User, Profile
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.




class LoginView(FormView):
    template_name = 'registration/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('root:home')


    def form_valid(self, form):
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user = authenticate(username = email, password = password)
        if user is not None:
            login(self.request, user)
            messages.add_message(self.request, messages.SUCCESS,"شما با موفقیت وارد شدید")
            return super().form_valid(form)   #redirect to success url
        else:
            messages.add_message(self.request,messages.ERROR, "اطلاعات شما معتبر نیست")
            return redirect(self.request.path_info)
        





class RegisterView(CreateView):
    template_name = 'registration/register.html'
    form_class = SignupForm

    def post(self, request, *args, **kwargs):
        data = request.POST
        email = data.get('email')
        if User.objects.filter(email=email).exists():
            messages.add_message(
                self.request, messages.ERROR, 'این ایمیل قبلا ثبت نام شده است'
            )
            return redirect(self.request.path_info)
        return super().post(request, *args, **kwargs)




    def form_valid(self, form):
        try:
            form.save()
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            user = authenticate(username = email,password = password)
            if user is not None:
                login(self.request, user)
                messages.add_message(self.request,messages.SUCCESS,'شما با موفقیت ثبت‌نام کردید')
                return redirect(f'/accounts/edit-profile/{user.id}/')
        except Exception as e:
            print(f"Error during registration: {e}")
            messages.add_message(self.request, messages.ERROR, 'خطایی در ثبت‌نام رخ داد')
            return redirect(self.request.path_info)
       
       

    def form_invalid(self, form):
        messages.add_message(self.request,messages.ERROR,'پسورد باید با حروف لاتین، 8 کارکتر ، ترکیبی از حروف بزرگ و کوچک و علائم باشد')
        return redirect(self.request.path_info)
    




class LogoutView(LoginRequiredMixin,TemplateView):
    def get(self, request, *args, **kwargs):
        logout(request)
        messages.add_message(self.request, messages.SUCCESS, "خروج شما با موفقیت انجام شد")
        return redirect("/")
    

class ViewProfile(LoginRequiredMixin,TemplateView):
    template_name = 'accounts/view-profile.html'



class UpdateProfileView(LoginRequiredMixin,TemplateView):
    template_name = 'accounts/edit-profile.html'
    form_class = EditProfileForm
    success_url = 'accounts/view-profile.html'

    # def get(self, request, *args, **kwargs):
    #     user = self.request.user
    #     if kwargs.get('pk') == user.id: #if the user is editing their own profile
    #         return super().get(request, *args, **kwargs) #all good proceed to render template
    #     else:
    #         messages.add_message(self.request, messages.ERROR,"شما اجازه ویرایش این پروفایل را ندارید.")
    #         return redirect ('/')

    def get(self, request, *args, **kwargs):
        user = self.request.user
        if (kwargs.get("pk") != user.id):  
            messages.error(self.request, "ما اجازه ویرایش این پروفایل را ندارید.")
            return redirect('/')
        return super().get(request, *args, **kwargs)
        
    def post(self, request, *args,**kwargs):
        profile = Profile.objects.get(user=request.user)
        mobile = profile.mobile
        id_code = profile.id_code
        if mobile =='' and id_code == '':
            form = self.form_class(request.POST, instance=profile)
            if form.is_valid():
                form.save()
                messages.success(self.request,"پروفایل شما با موفقیت ویرایش شد.")
                return redirect(self.success_url)
            else:
                messages.error(self.request,"کد ملی یا موبایل تکراری می باشد")
                return redirect(request.path_info)
        elif request.POST.get('mobile') != mobile:
            messages.error(self.request,"")
            return redirect(request.path_info)
        elif request.POST.get('id_code') != id_code:
            messages.error(self.request,"")
            return redirect(request.path_info)
        else:
            form = self.form_class(request.POST, instance=profile)
            if form.is_valid():
                form.save()
                messages.success(self.request,"پروفایل شما با موفقیت ویرایش شد.")
                return redirect(self.success_url)
            else:
                messages.error(self.request,"کد ملی یا موبایل تکراری می باشد")
                return redirect(request.path_info)



