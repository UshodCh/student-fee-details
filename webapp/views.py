from django.shortcuts import render,redirect,get_object_or_404
from django.views.decorators.cache import never_cache
from .models import student
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from .forms import studentform
# Create your views here.

def no_cache_login_required(view_func):
    return never_cache(login_required(view_func))
def loginuser(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')     # first page
        else:
            return render(request, 'login.html', {'error': 'Invalid login details'})

    return render(request, 'login.html')
@no_cache_login_required
def index(request):
    return render(request,'index.html')
@no_cache_login_required
@login_required(login_url='home')
def home(request):
    return render(request,'home.html')
@no_cache_login_required
def viewdata(request):
    return render(request,'viewdata.html')
@no_cache_login_required
def students_class(request,cls):
    students = student.objects.filter(cls=cls)
    return render(request, "students_class.html", {"students": students})
@no_cache_login_required
def update(request,reg):
    stu=get_object_or_404(student,reg=reg)
    if request.method == 'POST':
        # Get data from POST request
        name = request.POST['name']
        cls = request.POST['cls']
        reg_no = request.POST['reg']
        fee = request.POST['fee']

        # Optional: simple validation
        if name and cls and reg_no and fee:
            stu.name = name
            stu.cls = cls
            stu.reg = reg_no
            stu.fee = fee
            stu.save()  # Save changes to the database
            return redirect('viewdata')  # Redirect after update

        # If validation fails, you can add a message or pass an error to template
        error = "All fields are required."
        return render(request, 'update.html', {'student': stu, 'error': error})

    # For GET request, just render the form with existing student data
    return render(request, 'update.html', {'student': stu})
@no_cache_login_required
def delete(request,reg):
    stu=get_object_or_404(student,reg=reg)
    stu.delete()
    return redirect('viewdata')
@no_cache_login_required
def insert(request):
    if request.method=='POST':
        name = request.POST['name']
        cls = request.POST['cls']
        reg = request.POST['reg']
        fee = request.POST['fee']
        stu=student()
        form=studentform(request.POST,instance=stu)
        if form.is_valid():
            form.save()
            message = "Student added successfully!"
            return render(request,'home.html',{'message':message})
        else:
            print(form.errors)
    else:
        form=studentform()
    return render(request,'insert.html',{'form':form})