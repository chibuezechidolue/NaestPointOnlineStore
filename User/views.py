from django.shortcuts import render,redirect

from User.models import NewsLetterSubscribers
from .forms import CustomUserRegisterForm, NewsLetterForm,UpdateUserInfoForm,UpdatePasswordForm
from django.contrib import messages
from django.contrib.auth import authenticate, login ,logout,get_user
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect,HttpResponseForbidden



# def login_page(request):
#     form=LoginForm()
#     if request.method=="POST":
#         form=LoginForm(request.POST)
#         if form.is_valid():
#             email=form.cleaned_data.get("email")
#             password=form.cleaned_data.get("password")
#             print(email,password)
#             user = authenticate(request, email=email, password=password)
#             print(user)
#             if user is not None:
#                 login(request, user)
#                 print("user has been logged in")
#                 return redirect("home-page")
#             else:
#                 pass # find a way to tell the user that one or both the emai/username or password is incorrect

#         form=LoginForm(request.POST)
#     return render(request,"user/login.html",{"form":form})


# from django.http import HttpResponseRedirect
# def logout_page(request):
#     logout(request)
#     return HttpResponseRedirect(request.path_info)

def register_page(request):
    form=CustomUserRegisterForm()

    if request.method == "POST":
        form = CustomUserRegisterForm(request.POST)
        print(form)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "Your account has been created")
            return redirect("login-page")
        form=CustomUserRegisterForm(request.POST)
        
    return render(request,"user/register.html",{"form":form})



@login_required
def user_profile(request,option:str=None):
    arguement={}
    if option=="edit":
        form=UpdateUserInfoForm(instance=request.user)
        arguement={"form":form,"edit":True}
    elif option=="delete_account":
        arguement={"delete_account":True}
    
    # elif option=="change_password":
    #     form=UpdatePasswordForm()
    #     arguement={"form":form,"change_password":True}    

    if request.method=="POST":
        if option=="edit":
            form=UpdateUserInfoForm(request.POST,instance=request.user)
            if form.is_valid():
                form.save()
                messages.add_message(request, messages.SUCCESS, "Your details has been updated sucessfully")
                return redirect("user-profile")
        elif option == "delete_account":
            user=request.user
            user.delete()
            messages.add_message(request, messages.SUCCESS, "Your Account has been deleted successfully")
            return redirect("login-page")
        
            # View function for change password
        # elif option=="change_password":
        #     form=UpdatePasswordForm(request.POST,instance=request.user)
        #     if form.is_valid():
        #         print("form is valid")
        #         old_password=form.cleaned_data.get("password")
        #         user=authenticate(request,email=request.user.email,password=old_password)
        #         print(user)
        #         if user is not None:
        #             new_password1=form.cleaned_data.get("new_password1")
        #             new_password2=form.cleaned_data.get("new_password2")
        #             if new_password1==new_password2: #NOTE: change this line of code for security
        #                 form.save()
        #                 messages.add_message(request, messages.SUCCESS, "Your password has been changed sucessfully")
        #                 return redirect("user-profile")
    return render(request,"user/profile.html",arguement)

class ChangePasswordView(LoginRequiredMixin,PasswordChangeView):
    success_message = 'Your password has been changed successfully'
    template_name = "user/profile.html"


def subscribe_newsletter(request):
    if request.method=="POST":
        form=NewsLetterForm(request.POST)
        if form.is_valid():
            print('it is a valid form')
            form.save()
            messages.add_message(request, messages.SUCCESS, "Your subscription to newletter was successful")
        else:
            messages.add_message(request, messages.ERROR, "Your subscription to newletter was not successful")
        return redirect('home-page')
    return HttpResponseForbidden()

def unsubscribe_newsletter(request):
    sub_email=NewsLetterSubscribers.objects.get(email=request.GET.get('email'))
    sub_email.delete()
    return render(request,'user/unsubscribe-news.html')

        
    

