from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Posts, BlogComment,Categorys
from django.contrib import messages
from django.contrib.auth.models import User
from blog.templatetags import extras
from django.core.paginator import Paginator

# Create your views here.
def BlogHome(request):
    posts = Posts.objects.all()
    cat = Categorys.objects.all()
    #catPosts = Posts.objects.filter(cat=cat).all()
    paginator = Paginator(posts, 9)  # Show 25 contacts per page.
    
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    pagerange = paginator.num_pages
    pn = int(page_number)
  
    return render(request,'blog/news.html', {
        'allposts':page_obj,
        'page_obj':page_obj,
        'range': range(1,pagerange),
        'pageRange': paginator,
        'page_num':pn,
         'category':cat
        
        })

def cat(request,cat):
    print(cat)
    catPosts = Posts.objects.filter(cat=cat).all()
    catName = Categorys.objects.filter(id=cat).all().first()
    paginator = Paginator(catPosts, 6)  # Show 25 contacts per page.
    category = Categorys.objects.all()

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    pagerange = paginator.num_pages
   

    return render(request,'blog/cat.html',{
        'catP':page_obj,
        'page_obj':page_obj,
        'range': range(1,pagerange),
        'pageRange': paginator,
        'cat':catName,
        'id':cat,
        'post': catPosts,
        'category':category,
        
     })


def BlogPost(request, slug):
    #return HttpResponse(f'BlogPost {slug}')
    cat = Categorys.objects.all()
   
    post=Posts.objects.filter(slug=slug).first()
   
    category = Categorys.objects.all()
    allP = Posts.objects.all().order_by('-sno')
    cat_wise_post = Posts.objects.filter(cat=post.cat).order_by('-sno')[:3]
    post.views = post.views + 1
    post.save()


    comments= BlogComment.objects.filter(post=post, parent=None)
    replies= BlogComment.objects.filter(post=post).exclude(parent=None)
    replyDict={}
    for reply in replies:
        if reply.parent.sno not in replyDict.keys():
            replyDict[reply.parent.sno]=[reply]
        else:
            replyDict[reply.parent.sno].append(reply)
    #print(replyDict)

    context={"post":post, "comments":comments,'user':request.user, "replyDict":replyDict,
        "allposts":allP,'category':category,  'category':cat, 'cat_wise_post':cat_wise_post,
    }
    
    return render(request, 'blog/post.html', context)

def postComment(request):
    if request.method == "POST":
        comment=request.POST.get('comment')
        user=request.user
        postSno =request.POST.get('postSno')
        post= Posts.objects.get(sno=postSno)
        parentSno= request.POST.get('parentSno')
        if parentSno=="":
            comment=BlogComment(comment= comment, user=user, post=post)
            comment.save()
            messages.success(request, "Your comment has been posted successfully")
        else:
            parent= BlogComment.objects.get(sno=parentSno)
            comment=BlogComment(comment= comment, user=user, post=post , parent=parent)
            comment.save()
            messages.success(request, "Your reply has been posted successfully")
     
        
    return redirect(f"/blog/{post.slug}")


