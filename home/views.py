from django.shortcuts import render,HttpResponse,redirect
from .models import Contact
from django.contrib.auth.models import User
from blog.models import Posts,Categorys
from django.contrib.auth import authenticate,  login, logout
from django.contrib import messages
from blog.models import Posts
from django.core.paginator import Paginator
from django.conf import settings
from django.core.mail import send_mail


# Create your views here.
def home(request):
    post = Posts.objects.order_by('-sno')[:3]
    cat = Categorys.objects.all()
    
    allpost = Posts.objects.order_by('-sno')
    return render(request, 'blog/index.html',{
        'allposts':post,
        'catPosts':allpost,
        'category':cat
    })

def about(request):
    cat = Categorys.objects.all()
    return render(request, 'home/about.html',{
        'category':cat,
    })

def contact(request):

    cat = Categorys.objects.all()

    if request.method == "POST":
        name = request.POST.get('name','')
        email = request.POST.get('email','')
        phone = request.POST.get('phone','')
        content = request.POST.get('msg','')
        if len(name)<2 or len(email)<3 or len(content)<4:
            messages.error(request, "Please fill the form correctly")
        else:
            contact=Contact(name=name, email=email, phone=phone, content=content)
            contact.save()

            subject = f'Contact Form by {name}'
            message = f'{content} \n \n Name: {name} \n Email: {email} '
            email_from = email
            recipient_list = [settings.EMAIL_HOST_USER, 'purificationevan04@gmail.com','evangelmathew@gmail.com' ]
            send_mail(subject, message, email_from, recipient_list)
            messages.success(request, "Your message has been successfully sent")

     


    return render(request, 'home/contact.html',{
        'category':cat,
    })

def search(request):
    
    query=request.GET.get('query','')
    cat = Categorys.objects.all()

    if(len(query) > 78 ):
        allPosts = Posts.objects.none()

    else:
        allPosts= Posts.objects.filter(content__icontains=query)|Posts.objects.filter(title__icontains=query)|Posts.objects.filter(author__icontains=query)
   

    if(len(allPosts)==0):
        messages.warning(request, "No Search Matched")
        
    paginator = Paginator(allPosts, 3)  # Show 25 contacts per page.

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    pagerange = paginator.num_pages
    params={'allposts': allPosts, 'query':query,
        'page_obj':page_obj,
        'range': range(1,pagerange),
        'pageRange': paginator,
        'category':cat,
        
    }
    return render(request, 'blog/search.html', params)

    
   # return HttpResponse("This is Search")


def handleSignup(request):
    
    if request.method == 'POST':
        user = User.objects.all()
        
        # Get the post parameters
        username=request.POST['username']
        email=request.POST['email']
        fname=request.POST['fname']
        lname=request.POST['lname']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']

         # check for errorneous input
        if len(username)>12:
            messages.error(request, " Your user name must be under 12 characters")
            return redirect('/')
        if User.objects.filter(username = username).first():
            messages.error(request, "This username is already taken")
            return redirect('/')

        if not username.isalnum():
            messages.error(request, " User name should only contain letters and numbers")
            return redirect('/')
        if (pass1!= pass2):
             messages.error(request, " Passwords do not match")
             return redirect('/')

        #Create Users
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name= fname
        myuser.last_name= lname
        user=authenticate(username= username, password= pass1)
        login(request, user)
        myuser.save()
        messages.success(request, " Your iCoder has been successfully created")
        return redirect('/')
    else:
        return HttpResponse("404 - Not found")


def handeLogin(request):
    if request.method=="POST":
        # Get the post parameters
        loginusername=request.POST['loginusername']
        loginpassword=request.POST['loginpassword']

        user=authenticate(username= loginusername, password= loginpassword)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect("/")
        else:
            messages.error(request, "Invalid credentials! Please try again")
            return redirect("/")

    return HttpResponse("404- Not found")
   

    return HttpResponse("login")

def handelLogout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('/')

def profile(request, user):
    user = User.objects.filter(username=user).first()
    print(user)

    return render(request, 'home/profile.html' ,{'user':user})