from django.shortcuts import render, redirect
from django.contrib.auth import  logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages , auth
from django.core.paginator import Paginator
from .models import Account
from course.models import Course

def loginpage(request):
    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = auth.authenticate(email=email,password=password)
        
        if not user:
            try:
                user = auth.authenticate(email = email ,password=password)
            except:
                messages.error(request,"credential wrong")
                
        if user is not None:
            auth.login(request,user)
            return redirect('index')
            
        else:
            messages.error(request,"credential wrong")
    return render(request,'login.html')

@login_required (login_url='login')
def user_logout(request):
    logout(request)
    return redirect('login')

@login_required (login_url='login')
def index(request):
    return render(request, 'index.html')

def profile(request):
    return render(request,"profile.html")

@login_required(login_url='login')
def change_password(request) :
    if request.method == 'POST' :
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        user = Account.objects.get(email__exact = request.user.email)
        
        print(current_password)
        print(new_password)
        print(confirm_password)
        
        if new_password == confirm_password :
            success = user.check_password(current_password)
            print(success)
            if success :
                user.set_password(new_password)
                user.save()
                
                # logout(request) 
                
                messages.success(request, 'Password changed successfully')
                return redirect('viewAccount')
            else :
                messages.error(request, 'Please enter correct Current Password')
                return render('viewAccount')
        else :
            messages.error(request, 'New Password Does Not Match')
            return redirect('viewAccount')
        
    
    return render(request, 'profile.html')


def course(request):
    course = None
    course = Course.objects.all()     
    context = {
        'course' : course,
    }
    return render(request,"short-course-view.html",context)

def create_course(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        subtitle = request.POST.get('subtitle')
        description = request.POST.get('description')
        image = request.FILES.get('image')
        amount_v = request.POST.get('amout_v')
        amount_t = request.POST.get('amout_t')
        status_label = request.POST.get('category')
        
        categories = {
            'Enable': True,
            'Disable': False,
        }
        status = categories.get(status_label, 'Unknown')

        course = Course(title=title,
                        subtitle =subtitle,
                        image=image,
                        description=description,
                        amountinvalue=amount_v,
                        amountintext=amount_t,
                        status=status )
        course.save()

        return redirect('createcourse')
    
    return render(request,"short-course-create.html")



    
@login_required(login_url='login')
def update_course(request, id) :
    if request.user.is_authenticated:
        course = Course.objects.get(id=id)
        if request.method == 'POST' :
            course.title = request.POST.get('title')
            course.subtitle = request.POST.get('subtitle')
            course.description = request.POST.get('description')
            image = request.FILES.get('image')
            if image:
                course.image = image
            course.amount_v = request.POST.get('amout_v')
            course.amount_t = request.POST.get('amout_t')
            status_label = request.POST.get('category')
                
        categories = {
            'Enable': True,
            'Disable': False,
        }
        course.status = categories.get(status_label, 'Unknown')
        
        course.save()
        return redirect('course')
    
    return render(request,"update.html")
    
    

@login_required(login_url='login')
def delete_course(request,id):
    if request.user.is_authenticated:
        adminprod =  Course.objects.get(id=id)
        adminprod.delete()
        return redirect('course')
    else:
        return redirect("login")