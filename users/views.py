from django.shortcuts import render,redirect,HttpResponseRedirect,HttpResponse
from users.forms import UserRegistrationForm, UserProfileForm,UserUpdateForm,UserProfileUpdateForm
from django.contrib import messages
from django.contrib.auth.models import Group,User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login
from django.urls import reverse
# Create your views here.

def register(request):
    if request.method=='POST':
        u_form=UserRegistrationForm(request.POST)
        p_form=UserProfileForm(request.POST,request.FILES)
        if u_form.is_valid() and p_form.is_valid():
            check=User.objects.filter(email=u_form.cleaned_data.get('email')).exists()
            if check is False:
                user=u_form.save()      
                user.save()
                designation=p_form.cleaned_data.get('designation')
                if designation=='TEACHER':
                    group=Group.objects.get(name='Teacher')
                    user.groups.add(group)
                else:
                    group=Group.objects.get(name='Student')
                    user.groups.add(group)
                profile=p_form.save(commit=False)
                profile.user=user
                if 'profile_pic' in request.FILES:
                    profile.profile_pic=request.FILES['profile_pic']
                profile.save()
                messages.success(request,"Your account has been created. Log In")
                return redirect('login')
            else:
                messages.warning(request,"Email already exists")
                return redirect('register')
    else:
        u_form=UserRegistrationForm()
        p_form=UserProfileForm()
    context={'u_form':u_form,'p_form':p_form}
    return render(request,'users/signup.html',context)


def user_login(request):
    if request.method=="POST":
        username=request.POST.get("username")
        password=request.POST.get("password")
        user=authenticate(username=username,password=password)
        if user:
            if user.is_active:
                if user.profile.designation=='TEACHER':
                    login(request,user)
                    return HttpResponseRedirect(reverse('pdfs:teacher_dashboard'))
                else:
                    login(request,user)
                    return HttpResponseRedirect(reverse('pdfs:student_dashboard'))
            else:
                return HttpResponse("Account not active")
        else:
            return HttpResponse("Invalid account")
    else:
        return render(request,'users/login.html',{})

@login_required
def profile(request):
    if request.method=="POST":
        u_form=UserUpdateForm(request.POST,instance=request.user)
        p_form=UserProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request,"Your information has been updated")
            return redirect('profile')
    else:
        u_form=UserUpdateForm(instance=request.user)
        p_form=UserProfileUpdateForm(instance=request.user.profile)
        context={'u_form':u_form,'p_form':p_form}
    return render(request,'users/profile.html',context)
