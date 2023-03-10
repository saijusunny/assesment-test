from django.shortcuts import render,redirect
from django.contrib.auth.models import User, auth
from .models import Staff,Users,transaction,money
from . import models
from  django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import os

from django.contrib.auth import get_user_model

# Create your views here.
def login(request):
    return render(request,'login.html')
def signup(request):
    
    return render(request, 'signup.html')

@login_required(login_url='login')
def trans(request):
    ids=request.user.id
    if request.user.role=="USER":
        filt=Users.objects.get(id=ids)
        
    else:
        filt=Staff.objects.get(id=ids)
    dats=Users.objects.filter(role="USERS")
    snd_det=transaction.objects.filter(user=ids)
    req_det=money.objects.filter(user=ids)
    
    stf="STAFF"
   
    context={
        'filt':filt,
        "stf":stf,
        "req_det":req_det,
        "snd_det":snd_det,
        "dats":dats
    }

    return render(request, 'transaction.html',context)

@login_required(login_url='login')
def home(request):
    ids=request.user.id
    filt=Users.objects.get(id=ids)
    stf="STAFF"
    adm="ADMIN"
    return render(request, 'home.html',{'filt':filt,"stf":stf,"adm":adm})

def usercreate(request):
    if request.method=="POST":
        fname=request.POST['first_name']
        lname=request.POST['last_name']
        username=request.POST['username']
        password=request.POST['password']
        cpass=request.POST['cpassword']
        email=request.POST['email']
        role=request.POST['role']
        
        if request.FILES.get('file') is not None:
            image=request.FILES.get('file')
        else:
            image = "static/image/icon.png"
       
        if role=="Staff":
         
            if password==cpass:
                if Staff.objects.filter(username=username).exists():
                    messages.info(request, 'This Username Is Already Exists!!!!!')
                    return redirect('signup')
                else:
                    user=Staff.objects.create_user(
                        first_name=fname,
                        last_name=lname,
                        username=username,
                        password=password,
                        email=email,
                        image=image,
                    )
                    user.save()
            else:
                messages.info(request, 'Password doesnot match!!!!!')
                return redirect('signup')
        else:
            if password==cpass:
                if Users.objects.filter(username=username).exists():
                    messages.info(request, 'This Username Is Already Exists!!!!!')
                    return redirect('signup')
                else:
                    user=Users.objects.create_user(
                        first_name=fname,
                        last_name=lname,
                        username=username,
                        password=password,
                        email=email,
                        image=image,
                    )
                    user.save()
            else:
                messages.info(request, 'Password doesnot match!!!!!')
                return redirect('signup')

        return redirect('login')
    else:
        return redirect('signup')


def adminlogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        
        user = authenticate(username=username,password=password)
        
        if user is not None:
            if user.is_active:
                auth.login(request,user)   
                return redirect('home')
        else:
            messages.info(request, 'invalid username and password, try again')
            return redirect('login')
    else:
        return redirect('login')

@login_required(login_url='login')
def user_management(request):
    ids=request.user.id
    role=request.user.role
    
    if role=="USER":
    
        filt=Users.objects.get(id=ids)
    else:
        filt=Staff.objects.get(id=ids)
    dats=Users.objects.filter(role="USERS")


    
    file="/static/image/icon.png"
    stf="STAFF"
    adm="ADMIN"
  
    return render(request, 'usermanagement.html',{'filt':filt,"stf":stf,"adm":adm,"dats":dats,"file":file})

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('login')

@login_required(login_url='login')
def editpro(request,pk):
    
    if request.method=='POST':
       
        role=request.user.role
      
        if role=="STAFF":
            stf = Staff.objects.get(id=request.user.id)
            fname=request.POST['first_name']
            lname=request.POST['last_name']
            username=request.POST['username']
            password=request.POST['password']
            cpass=request.POST['cpassword']
            email=request.POST['email']
            if password==cpass:
                if password=="":
                    created = Staff.objects.filter(id=request.user.id).update(first_name=fname,last_name=lname,username=username,email=email)
                    return redirect('user_management')
                else: 
                    created = Staff.objects.filter(id=request.user.id).update(first_name=fname,last_name=lname,username=username,email=email,password=password)
                    redirect('login')

            else:
                messages.info(request,f"Check Entered Password And Confirm Password")
        else:
            
            stf = Users.objects.get(id=request.user.id)
            
            fname=request.POST.get('first_name')
            lname=request.POST.get('last_name')
            username=request.POST.get('username')
            password=request.POST.get('password')
            cpass=request.POST.get('cpassword')
            email=request.POST.get('email')
           
            if password==cpass:
                if password=="":
                  
                    created = Users.objects.filter(id=request.user.id).update(first_name=fname,last_name=lname,username=username,email=email)
                    
                    return redirect('user_management')
                else:
                    
                    created = Users.objects.filter(id=request.user.id).update(last_name=lname,username=username,email=email)
                    u = Users.objects.get(id=request.user.id)
                    u.set_password(password)
                    u.save() 
                    return redirect('login')
            else:
                messages.info(request,f"Check Entered Password And Confirm Password")
                return redirect('user_management')

        
    return redirect('user_management')
@login_required(login_url='login')
def send_mny(request,id):
    if request.method == 'POST':
            snd=transaction.objects.create(
                user=request.user,
                name=request.POST['name'],
                accountno=request.POST['acc_no'],
                branch=request.POST['branch'],
                name2=request.POST['name2'],
                accountno2=request.POST['acc_no2'],
                branch2=request.POST['branch2'],
                ammount=request.POST['amount'],

            )
            snd.save()

            
            return redirect("trans")
   
    return redirect("trans")
@login_required(login_url='login')
def req_mny(request,id):
    if request.method == 'POST':
            snd=money.objects.create(
                user=request.user,
                name=request.POST['name'],
                accountno=request.POST['acc_no'],
                branch=request.POST['branch'],
                name2=request.POST['name2'],
                accountno2=request.POST['acc_no2'],
                branch2=request.POST['branch2'],
                ammount=request.POST['amount'],

            )
            snd.save()

            
            return redirect("trans")
   
    return redirect("trans")
@login_required(login_url='login')
def view_user(request,id):
    snd_det=transaction.objects.filter(user=id)
    req_det=money.objects.filter(user=id)

    return render(request, "view_user.html", {"req_det":req_det,"snd_det":snd_det})

@login_required(login_url='login')
def up_pro(request,id):
    if request.method=="POST":
       
        User = get_user_model()
        pro = User.objects.get(id=id)
        if request.FILES.get('file') is not None:
            image=request.FILES['file']
        else:
            image = "static/image/icon.png"
        # created = User.objects.filter(id=request.user.id).update(image=image)
        os.remove(pro.image.path)
        pro.image=image
        pro.save()
        # created = User.objects.filter(id=id).update(image=image)

        return redirect('user_management')
    else:
        return redirect('user_management')