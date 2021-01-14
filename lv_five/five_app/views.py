from django.shortcuts import render,redirect
from five_app.forms import UserForm,UserProfileInfoForm

#
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect,HttpResponse
#from django.core.urlresolvers import reverse  #in newrversion dont need to import this
from django.contrib.auth.decorators import login_required
# Create your views here.
def index(request):
    return render(request,"five_app/index.html")

@login_required
def special(request):
    return HttpResponse("you are logged in NICE!")


@login_required
def user_logout(request):
    logout(request)
    return redirect("index")

def register(request):

    registered=False

    if request.method == 'POST':
        user_form=UserForm(data=request.POST)
        profile_form=UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():

            user=user_form.save()
            user.set_password(user.password)
            user.save()

            profile=profile_form.save(commit=False)
            profile.user=user #UserProfileInfoForm onetoone relation with User

            if 'profile_pic' in request.FILES: #to find the file it used when uplod any kind of file
                profile.profile_pic=request.FILES['profile_pic']

            profile.save()
            registered=True

        else:
            print(user_form.errors,profile_form.errors)

    else:
        user_form=UserForm()
        profile_form=UserProfileInfoForm()

    return render(request,"five_app/registration.html",{'user_form':user_form,
                                                        'profile_form':profile_form,
                                                        'registered':registered})



def user_login(request): #name of view cannot be equal to imported functions
    if request.method=='POST':
        username=request.POST.get('username') #grab data from html
        password=request.POST.get('password')

        user=authenticate(username=username,password=password) #chek provided data is True or not

        if user:
            if user.is_active:
                login(request,user) #login
                return redirect('index') #redirect the user to whatever the page you provide

            else:
                return HttpResponse("Account not active")

        else:
            print("someone try to login and failled")
            print("Username: {} and password: {} is not riht".format(username,password))
            return HttpResponse("invalid login details ")
    else:
        return render(request,'five_app/login.html',{})
