from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from django.views import View
from Profile.models import Profile,  Follow
from .forms import LoginForm, RegisterForm, CheckOtpForm, ResetPasswordRequestForm, ResetPasswordForm, OtpLoginForm, CheckOtpCodeForm
from random import randint
import ghasedakpack
from django.core import signing
import time
from .models import Otp, User, OtpCode

SMS = ghasedakpack.Ghasedak('')


class UserLoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('profile:feed')
        form = LoginForm()
        return render(request, 'Account/login.html', context={'form': form})


    def post(self,request):
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['phone'], password=cd['password'])
            if user is not None:
                login(request, user)
                return redirect("profile:feed")
            else:
                form.add_error('password',"Incorrect Username or Password")
        else:
            form.add_error(None,"information not found")
        return render(request, 'Account/login.html', context={'form': form})

class UserLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('account:login')


class RegisterView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('profile:feed')
        form = RegisterForm()
        return render(request, 'Account/register.html', context={'form': form})


    def post(self,request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            randcode = randint(10000,99999)
            print(randcode)
            SMS.verification({'receptor': cd['phone'], 'type': '1', 'template': 'randcode', 'param1': randcode})

            token_data = {'phone': cd['phone'], 'username': cd['username'], 'fullname': cd['fullname'], 'email': cd['email']}
            token = signing.dumps(token_data)
            if User.objects.filter(phone=cd['phone']).exists():
                form.add_error('phone',f"User Phone {cd['phone']} already exists")
            elif User.objects.filter(username=cd['username']).exists():
                form.add_error('username', f"User Name {cd['username']} already exists")
            else:
                Otp.objects.create(phone=cd['phone'], code=randcode, token=token)
                return redirect(reverse('account:check_otp') + f'?token={token}')
        else:
            form.add_error('phone',"information not found")
        return render(request, 'Account/register.html', context={'form': form})



class CheckOtpView(View):
    def get(self, request):
        form = CheckOtpForm()
        return render(request, 'Account/check_otp.html', context={'form': form})


    def post(self,request):
        token = request.GET.get('token')
        if not token:
            return redirect('account:register')
        try:

            user_data = signing.loads(token)
        except signing.BadSignature:
            return redirect('account:register')

        form = CheckOtpForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if Otp.objects.filter(code=cd['code'], phone=user_data['phone']).exists():
                user, is_created = User.objects.get_or_create(phone=user_data['phone'],username=user_data['username'], fullname=user_data['fullname'], email=user_data['email'])
                if Profile.objects.filter(user=user).exists() and Follow.objects.filter(user=user).exists():
                    login(request, user)
                    return redirect('profile:feed')
                else:
                   Profile.objects.create(user=user)
                   Follow.objects.create(user=user)
                   login(request, user)
                return redirect('profile:feed')
        return render(request,'Account/check_otp.html', context={'form': form})





class ResetPasswordRequestView(View):
    def get(self, request):
        form = ResetPasswordRequestForm()
        return render(request, 'Account/reset_password_request.html', context={'form': form})


    def post(self,request):
        form = ResetPasswordRequestForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            randcode = randint(10000, 99999)
            print(randcode)
            SMS.verification({'receptor': cd['phone'], 'type': '1', 'template': 'randcode', 'param1': randcode})

            token_data = {'phone' : cd['phone']}
            token = signing.dumps(token_data)
            if User.objects.filter(phone=cd['phone']).exists():
                Otp.objects.create(phone=cd['phone'], code=randcode, token=token)
                return redirect(reverse('account:reset_password_confirm') + f'?token={token}')
            else:
                form.add_error('phone',"شما ثبت نام نیستید")
                return redirect('account:reset_password_request')
        else:
            form.add_error('phone',"Phone Number is invalid")

            return render(request, 'Account/reset_password_request.html', context={'form': form})




class ResetPasswordConfirmView(View):
    def get(self, request):
        form = CheckOtpForm()
        return render(request, 'Account/reset_password_confirm.html', context={'form': form})

    def post(self, request):
        token = request.GET.get('token')
        if not token:
            return redirect('account:reset_password_request')
        try:
            user_data = signing.loads(token)
        except signing.BadSignature:
            return redirect('account:reset_password_request')

        form = CheckOtpForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if Otp.objects.filter(code=cd['code'], phone=user_data['phone']).exists():
                return redirect(reverse('account:reset_password_complete') + f'?token={token}')
        return render(request, 'Account/reset_password_confirm.html', context={'form': form})







class ResetPasswordCompleteView(View):
    def get(self, request):
        form = ResetPasswordForm()
        return render(request, 'Account/reset_password_complete.html', context={'form': form})

    def post(self, request):
        token = request.GET.get('token')
        if not token:
            return redirect('account:reset_password_request')
        try:
            user_data = signing.loads(token)
        except signing.BadSignature:
            return redirect('account:reset_password_request')

        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = User.objects.get(phone=user_data['phone'])
            user.set_password(cd['password'])
            user.save()
            login(request, user)
            return redirect('profile:home')
        return render(request, 'Account/reset_password_complete.html', context={'form': form})


class OtpLoginView(View):
    def get(self, request):
        form = OtpLoginForm()
        return render(request, 'Account/otp_login.html', context={'form': form})

    def post(self, request):
        form = OtpLoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            randcode = randint(10000, 99999)
            print(randcode)
            SMS.verification({'receptor': cd['phone'], 'type': '1', 'template': 'randcode', 'param1': randcode})
            token_data = {'phone': cd['phone']}
            token = signing.dumps(token_data)
            if User.objects.filter(phone=cd['phone']).exists():
                OtpCode.objects.create(phone=cd['phone'], code=randcode, token=token)
                return redirect(reverse('account:check_otp_login') + f'?token={token}')
            else:
                form.add_error('phone', "User does not exist")
                time.sleep(3)
                return redirect('account:register')

        return render(request, 'Account/otp_login.html', context={'form': form})


class CheckOtpLoginView(View):
    def get(self, request):
        form = CheckOtpCodeForm()
        return render(request, 'Account/check_otp_login.html', context={'form': form})

    def post(self, request):
        token = request.GET.get('token')
        user_data = signing.loads(token)

        form = CheckOtpCodeForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if OtpCode.objects.filter(code=cd['code'], phone=user_data['phone']).exists():
                user = User.objects.get(phone=user_data['phone'])

                login(request, user)
                return redirect('home:home')
        return render(request, 'Account/check_otp_login.html', context={'form': form})
