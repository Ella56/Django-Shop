from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import FormView,CreateView, TemplateView, UpdateView, ListView
from .forms import LoginForm, SignupForm, EditProfileForm, AddressForm, ResetPassForm,ResetPassConfirmForm,ChangePassForm
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import User, Profile, Province, City
from product.models import Product, Compare, Favorites
from django.contrib.auth.mixins import LoginRequiredMixin
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from rest_framework_simplejwt.tokens import RefreshToken,AccessToken
from threading import Thread
from .concurrency_processing  import send_mail
from django.contrib.auth.password_validation import validate_password


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
        





class SignupView(CreateView):
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
        form.save()
        data = form.cleaned_data
        email = data['email']
        password = data['password1']
        user = authenticate(username=email, password=password)
        if user is not None:
            login(self.request, user)
        messages.add_message(
            self.request,
            messages.SUCCESS,
            'ثبت نام موفقیت آمیز . لطفا مشخصات کاربری خود را تکمیل نمایید',
        )
        return redirect(f'/accounts/edit-profile/{user.id}/')

       
       

    def form_invalid(self, form):
        messages.add_message(self.request,messages.ERROR,'پسورد باید با حروف لاتین، 8 کارکتر ، ترکیبی از حروف بزرگ و کوچک و علائم باشد')
        return redirect(self.request.path_info)
    




class LogoutView(LoginRequiredMixin,TemplateView):

    def get(self, request, *args, **kwargs):
        logout(request)
        messages.add_message(self.request, messages.SUCCESS, "خروج شما با موفقیت انجام شد")
        return redirect("/")
    

class ViewProfile(LoginRequiredMixin,TemplateView):
    template_name = 'registration/view-profile.html'
    login_url = reverse_lazy('accounts:login')



class UpdateProfileView(LoginRequiredMixin,TemplateView):
    template_name = 'registration/edit-profile.html'
    form_class = EditProfileForm
    success_url = '/accounts/view-profile/'

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



class SetAddressView(LoginRequiredMixin, CreateView):
    template_name = 'registration/addresses.html'
    form_class = AddressForm
    success_url = '/accounts/profile/addresses'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['provinces'] = Province.objects.all()
        return context
    


    def form_valid(self, form):
        form.save()
        messages.add_message(self.request, messages.success, 'آدرس شما با موفقیت ثبت شد.')
        return redirect(self.success_url)
    


    def post(self, request, *args, **kwargs):
        user = self.request.user
        profile_id = get_object_or_404(Profile, user=user).id
        if request.POST.get('profile')  != str(profile_id):
            messages.error(self.request, "شما مجاز به ویرایش این پروفایل نیستید")
        return super().post(request, *args ,**kwargs)



    def form_invalid(self, form):
        messages.add_message(self.request, f"{form.errors}")
        return redirect(self.request.path_info)
    


    

def get_city(request):
    province_id = request.GET.get('province_id')
    if province_id:
        cities = City.objects.filter(province = province_id).values('id','name')
        return JsonResponse(list(cities), safe=False)
    return JsonResponse([] ,safe=False)


class ResetPassword(FormView):
    success_url = '/accounts/reset-password-done/'
    template_name = 'registration/forget-password.html'
    form_class = ResetPassForm


    def form_valid(self, form):
        email = form.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            token = self.get_token_for_user(user)
            t1 = Thread(target=send_mail, args=('email/email.html', user, token,"admin@my-site.com", user.email),)
            t1.start()
            messages.add_message(self.request,messages.SUCCESS,'ایمیل بازیابی رمز عبور ارسال شد',)
            return super().form_valid()
        else:
            messages.add_message(self.request, messages.ERROR, 'این ایمیل در سیستم وجود ندارد')
            return redirect(self.request.path_info)
        
    def get_token_for_user(self,user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    

class ResetPasswordDone(TemplateView):
    template_name = 'registrations/forget-password-done.html'


class ResetPasswordConfirm(FormView):
    template_name = 'registration/forget-password-confirm.html'
    form_class = ResetPassConfirmForm
    success_url = '/accounts/reset-password-complete/'

    def form_valid(self, form):
        password1 = form.cleaned_data['password1']
        password2 = form.cleaned_data['password2']

        if password1 == password2:
            try:
                validate_password(password1)
            except Exception as e:
                messages.error(self.request,"پسورد باید 8 کارکتر شامل حروف بزرگ و کوچک و علائم باشد  ",)
                return redirect(self.request.path_info)
            token = self.kwargs.get('token')
            try:
                access_token = AccessToken(token)
                user_id = access_token['user_id']
                user = User.objects.get(id=user_id)
                user.set_password(password1)
                user.save()
                messages.add_message(self.request,messages.SUCCESS,'رمز عبور با موفقیت تغییر یافت',)
                return super().form_valid(form)
            except Exception as e:
                messages.error(self.request, "توکن منقضی شده است")
                return redirect('/accounts/reset-password/')
        else:
            messages.error(self.request, "پسوردها با هم مطابقت ندارند")
            return redirect(self.request.path_info)



class ResetPasswordComplete(TemplateView):
    template_name = 'registrations/forget-password-complete.html'


class ChangePassword(LoginRequiredMixin, FormView):
    template_name = 'registration/change-password.html'
    form_class = ChangePassForm
    success_url = '/accounts/view-profile/'


    def form_valid(self, form):
        old_password = form.cleaned_data['old_password']
        user = self.request.user
        if not user.check_password(old_password):
            messages.error(self.request, "پسورد قدیمی صحیح نمیباشد")
            return redirect(self.request.path_info)
        password1 = form.cleaned_data['password1']
        password2 = form.cleaned_data['password2']
        if password1 == password2:
            try:
                validate_password(password1)
            except Exception as e:
                messages.error(self.request,"پسورد باید 8 کارکتر شامل حروف بزرگ و کوچک و علائم باشد  ",)
                return redirect(self.request.path_info)
            user.set_password(password1)
            user.save()
            messages.add_message(self.request, messages.SUCCESS,'رمز عبور با موفقیت تغییر یافت',)
            return super().form_valid(form)
        else:
            messages.error(self.request, "پسوردها با هم مطابقت ندارند")
            return redirect(self.request.path_info)
        


    def form_invalid(self, form):
        messages.error(self.request, f"{form.errors}")
        return redirect(self.request.path_info)



class CompareView(LoginRequiredMixin,ListView):
    template_name = 'registration/compare.html'
    model = Compare
    context_object_name = 'comparisons'



    def get_queryset(self):
        user = self.request.user
        profile = get_object_or_404(Profile, user=user)
        comparisons = Compare.objects.filter(name=profile)
        return comparisons
    

@csrf_exempt
def compare_create(request):
    if not request.user.is_authenticated:
        return JsonResponse({"success": False, "message": "ابتدا وارد شوید!"}, status=400)
    if request.method == "POST":
        data = json.loads(request.body)
        product_id = data.get('product_id')
        user = request.user
        profile = get_object_or_404(Profile, user=user)
        product = Product.objects.get(id=product_id)
        try:
            Compare.objects.get(name=profile,  product=product)
            return JsonResponse({"message": "این محصول قبلا اضافه شده است!"}, status=400)
        except Compare.DoesNotExist:
            Compare.objects.create(name=profile,product=product)
            return JsonResponse({"message": "محصول اضافه شد!"}, status=200)
    return JsonResponse({"message": "خطای نا مشخص!"}, status=400)

@csrf_exempt
def compare_remove(request):
    if not request.user.is_authenticated:
        return JsonResponse({"success": False, "message": "ابتدا وارد شوید!"}, status=400)
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            product_id=data.get('product_id')
            user=request.user
            profile = get_object_or_404(Profile, user=user)
            product = Product.objects.get(id=product_id)
            compare = Compare.objects.get(name=profile,product=product)
            compare.delete()
            return JsonResponse({"success": True, "message": "محصول حذف شد!"}, status=200)
        except Exception as e:
            return JsonResponse({"success": False,"message": "خطایی رخ داد . یکبار صفحه را رفرش کنید!"},status=400)
    return JsonResponse({"message": "متد غیرمجاز!"}, status=405)


class FavoriteView(LoginRequiredMixin, ListView):
    template_name = 'registration/favorites.html'
    model = Favorites
    context_object_name = 'favorites'


    def get_queryset(self):
        user = self.request.user
        profile = get_object_or_404(Profile,user=user)
        favorites = Favorites.objects.filter(name=profile)
        return favorites
    

@csrf_exempt
def favorites_create(request):
    if not request.user.is_authenticated:
        return JsonResponse({"success": False, "message": "ابتدا وارد شوید!"}, status=400)
    if request.method == 'POST':
        data = json.loads(request.body)
        product_id = data.get('product_id')
        user = request.user
        profile = get_object_or_404(Profile, user=user)
        product = Product.objects.get(id = product_id)
        try:
            Favorites.objects.get(name=profile,product=product)
            return JsonResponse({"message": "این محصول قبلا اضافه شده است!"}, status=400)
        except Favorites.DoesNotExist:
            Favorites.objects.create(name=profile,product=product)
            return JsonResponse({"message": "محصول اضافه شد!"}, status=200)

    return JsonResponse({"message": "خطای نا مشخص!"}, status=400)

@login_required
def favorites_remove(request, pk):
    try:
        user = request.user
        profile = get_object_or_404(Profile,user=user)
        product = Product.objects.get(id=pk)
        favorites = Favorites.objects.get(name=profile,product=product)
        favorites.delete()
        messages.success(request, 'محصول حذف شد')
        return redirect('accounts:user-favorites')
    except Exception as e:
        messages.error(request, 'خطایی رخ داد . یکبار صفحه را رفرش کنید!')
        return redirect('accounts:user-favorites')