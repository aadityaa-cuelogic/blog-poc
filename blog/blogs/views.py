from django.shortcuts import render, render_to_response

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import RequestContext
from blogs.forms import RegistrationForm, CreatePostForm
from django.contrib.auth.models import User
from .models import Post, Comment, Category
import datetime
from django.utils import timezone
# Create your views here.

# home page method
# @login_required(login_url="login/")
def home(request):
    latest_blog_post = Post.objects.order_by('-created_on')[:5]
    category = Category.objects.all()
    context = {'latest_blog_post': latest_blog_post, 'category':category}
    return render(request, "home.html", context)

# def handle_uploaded_file(f):
#     with open('some/file/name.txt', 'wb+') as destination:
#         for chunk in f.chunks():
#             destination.write(chunk)

def createPost(request):
    if request.method == 'POST':
        form = CreatePostForm(request.POST)
        if form.is_valid():
            try:
                post = Post.objects.create(
                    title=form.cleaned_data['title'],
                    body=form.cleaned_data['description'],
                    category=form.cleaned_data['category'],
                    author=request.user
                )
            except Post.DoesNotExist:
                raise HttpResponse('Blog create failed !!!')
            return HttpResponse("Success in form")
            # return render(request, "create_post.html")
        else:
            return render(request, 'create_post.html', {'form': form})
    else:
        context = {'form':CreatePostForm() }
        return render(request, 'create_post.html', context)

def createPostSuccess(request):
    return HttpResponse("Error in form")


# method to show blog post details page
def detailPost(request, slug):
    try:
        post = Post.objects.get(slug=slug)
        comment = Comment.objects.filter(post=post.id).order_by('-created_on')[:5]
        category = Category.objects.all()
    except Post.DoesNotExist:
        raise Http404("Blog does not exist")
    return render(request, 'detail_post.html', {'blog_post': post,
                'category':category, 'comment':comment})

# method to register user
@csrf_protect
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        # return HttpResponse("You're looking at question %r" % form)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
                email=form.cleaned_data['email']
            )
            return HttpResponseRedirect('/register/success/')
        else:
            context = {'form':form }
            return render(request, 'register.html', context)

    else:
        context = {'form':RegistrationForm() }
        return render(request, 'register.html', context)

# method after registration success to show success page
def register_success(request):
    return render_to_response('register_success.html', )
