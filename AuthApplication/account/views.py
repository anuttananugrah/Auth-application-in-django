from django.shortcuts import render,redirect
from django.views import View
from account.forms import *
from account.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login,logout
# Create your views here.

def send_otp(user_instance):
    user_instance.generate_otp()

    send_mail(
        subject='Django App Authentication - otp',
        message=f'Your Generated OTP is : {user_instance.otp}',
        from_email='anuttananugrah@gmail.com',
        recipient_list=[user_instance.email],
        fail_silently=True

    )

class SignUpView(View):
    def get(self,request):
        data=UserModelForm()
        return render(request,'registration.html',{'form':data})
    def post(self,request):
        form_data=UserModelForm(data=request.POST)
        if form_data.is_valid():
            user=form_data.save(commit=False)
            user.is_active=False
            user.save()
            send_otp(user)
            return redirect('otpverify')
        return render(request,'registration.html',{'form':form_data})

class OtpVerificationView(View):
    def get(self,request):
        return render(request,'otp_verify.html')
    def post(self,request):
        otpvl=request.POST.get('otpnum')
        try:
            user_instance=User.objects.get(otp=otpvl)
            user_instance.is_verified=True
            user_instance.is_active=True
            user_instance.otp=None
            user_instance.save()
            messages.success(request,'OTP verified successfully')
            return redirect('loginpage')
        except:
            return redirect('otpverify')
        
class UserHomeView(View):
    def get(self,request):
        return render(request,'userhome.html')



class LoginView(View):
    def get(Self,request):
        forms=LoginForm()
        return render(request,'loginpage.html',{'form':forms})
    def post(self,request):
        data_form=LoginForm(data=request.POST)
        if data_form.is_valid():
            username=data_form.cleaned_data.get('username')
            password=data_form.cleaned_data.get('password')
            user=authenticate(request,username=username,password=password)
            if user:
                login(request,user)
                messages.success(request,'Login Success')
                return redirect('userhome')
            else:
                messages.warning(request,'Invalid Username or Password')
                return redirect('loginpage')
        messages.error(request,'invalid input recieved')
        return render(request,'loginpage.html',{'form':data_form})
            
    
class ProfileView(View):
    def get(self,request):
        form=ProfileForm(instance=request.user.userprofile)
        return render(request,"profile.html",{'form':form})
    def post(self,request):
        form_data=ProfileForm(data=request.POST,files=request.FILES,instance=request.user.userprofile)
        if form_data.is_valid():
            form_data.save()
            messages.success(request,"Profile updated")
            return redirect('userhome')
        return render(request,"profile.html",{'form':form_data})
    
class LogOutView(View):
    def get(self,request):
        logout(request)
        messages.success(request,'User Loged Out!')
        return redirect('loginpage')
    

