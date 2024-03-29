from django.shortcuts import render,redirect
from .forms import RegistrationForm
from .models import Account,MyAccountManager
from django.contrib import messages,auth
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage




@csrf_exempt
def register(request):
    if request.method=='POST' :
        form= RegistrationForm(request.POST)
        if form.is_valid():
            first_name=form.cleaned_data['first_name']
            last_name=form.cleaned_data['last_name']
            phone_number=form.cleaned_data['phone_number']
            email=form.cleaned_data['email']
            password=form.cleaned_data['password']
            username=email.split("@")[0]
            user=Account.object.create_user(first_name=first_name,last_name=last_name,email=email,username=username,password=password)
            user.phone_number=phone_number
            user.save()
            current_site= get_current_site(request)
            mail_subject='Please activate your account'
            message=render_to_string('accounts/account_verification_mail.html',{
                'user':user,
                'domain':current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user),
            })
            to_email=email
            send_email=EmailMessage(mail_subject,message,to=[to_email])
            send_email.send()
           # messages.success(request,'Thank you for registrating wahith us,we have sent you a verification email to your email address ,Please verify it . ')
            return redirect('/accounts/login?command=verification&email='+email)
            
    else:
        form = RegistrationForm()
    context={
         'form':form,
     }
    return render(request,'accounts/register.html',context)
@csrf_exempt
def login_user(request):
    if request.method =='POST' :
        email=request.POST.get('email')
        password=request.POST.get('password')
        user=auth.authenticate(email=email,password=password)
        if user is not None:
            auth.login(request,user)
            messages.success(request,'You are now logged in.')
            return redirect('dashboard')
        else :
            messages.error(request,'Invailed login credent')
            return redirect('login')
    
    return render(request,'accounts/login.html')
@csrf_exempt
@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request,' You are logeed out')
    return redirect('login')
    #return render(request,'accounts/logout.html')
@csrf_exempt
def activate(request,uidb64,token):
    try :
       uid=urlsafe_base64_decode(uidb64).decode()
       user=Account._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,Account.DoesNotExist):
       user=None
    if user is not None and default_token_generator.check_token(user,token):

        user.is_active=True
        user.save()
        messages.success(request,'Congratulations Your account is activated')
        return redirect('login') 
    else:
        messages.error(request,'Invailid activation link')
        return redirect('register') 

def dashboard(request)  :
    return render(request,'accounts/dashboard.html')       
def forgetpassword(request)  :
    if request.method== 'POST':
        email=request.POST.get('email')
        if Account.object.filter(email=email).exists():
            user=Account.object.get(email__exact=email)
            current_site= get_current_site(request)
            mail_subject='Reaset Your Password'
            message=render_to_string('accounts/reset_password_email.html',{
                'user':user,
                'domain':current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user),
            })
            to_email=email
            send_email=EmailMessage(mail_subject,message,to=[to_email])
            send_email.send()
            messages.success(request,'Password reset email has sent to your mail addresse.')
            return redirect('login')
        else:
            messages.error(request,'Account does not exist')
            return redirect('forgetpassword')
    return render(request,'accounts/forgetpassword.html') 
def resetpassword_validation(request,uidb64,token):
    try :
       uid=urlsafe_base64_decode(uidb64).decode()
       user=Account._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,Account.DoesNotExist):
        user=None
    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid']=uid
        messages.success(request,'Please reset You password')
        return redirect('resetpassword')
    else:
        messages.error(request,'this  link has been expired')
        return redirect('login') 
        
def resetpassword(request):
    if request.method == 'POST' :
        password=request.POST.get('password')
        confirm_password=request.POST.get('confirm_password')

        if password == confirm_password :
            uid=request.session.get('uid')
            user=Account.object.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request,'Password reset successful')
            return redirect('login')

        else:
            messages.error(request,'Password do not match!')
            return redirect('resetpassword')
    else:   
        return render(request,'accounts/resetpassword.html')
# Create your views here.
