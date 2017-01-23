from django.shortcuts import render, render_to_response, redirect

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import RequestContext
from blogs.forms import RegistrationForm, CreatePostForm, MyProfileForm
from django.contrib.auth.models import User
from .models import Post, Comment, Category, Likes
import datetime
import json
from django.utils import timezone
# Create your views here.

# home page method
# @login_required(login_url="login/")
def home(request):
    latest_blog_post = Post.objects.order_by('-created_on')[:5]
    category = Category.objects.all()
    context = {'latest_blog_post': latest_blog_post, 'category':category}
    return render(request, "home.html", context)

def updateProfile(request, username=None):
    if request.method == "POST":
        if (
            username is not None or
            request.POST['first_name'] is not None  or
            request.POST['last_name'] is not None
           ):
                first_name = request.POST['first_name']
                last_name = request.POST['last_name']
                try:
                    user = User.objects.get(username=username)
                    loggedUser = request.user
                except User.DoesNotExist:
                    return HttpResponseRedirect('/logout/')
                if user.id == loggedUser.id:
                    updateUser = User.objects.filter(username=username).update(first_name=first_name, last_name=last_name)
        else:
            return HttpResponseRedirect('/logout/')
    return HttpResponseRedirect('/user/'+username+'/profile')

# function to get user profile
def userProfile(request, username=None):
    if request.method == 'GET':
        if username is not None:
            try:
                user = User.objects.get(username=username)
                category = Category.objects.all()
                post = Post.objects.filter(author=user)
                loggedUser = User.objects.get(pk=request.user.id)
                update_profile = False
                if user.id == loggedUser.id:
                    update_profile = True

                if user.first_name is None:
                    first_name='FirstName'
                else:
                    first_name=user.first_name
                if user.last_name is None:
                    last_name='LastName'
                else:
                    last_name=user.last_name

                form_data = {
                    'first_name': first_name,
                    'last_name':last_name,
                    'username':user.username,
                    'email':user.email
                }
                myprofileform = MyProfileForm(form_data)
            except User.DoesNotExist:
                raise Http404("User does not exist")
            context = {
                        'latest_blog_post': post,
                        'category':category,
                        'username':username,
                        'myprofileform':myprofileform,
                        'update_profile':update_profile
                    }
            return render(request, 'user_profile.html', context)
        else:
            raise Http404("User does not exist")
    else:
        raise Http404("User does not exist")

# return count of likes for a certain post
def getLikesCount(post_id):
    try:
        likes = Likes.objects.filter(post_id=post_id).count()
    except Likes.DoesNotExist:
        return 0
    return likes

# like - unlike blog post
@csrf_exempt
@login_required(login_url="/login/")
def likePost(request):
    if request.method == 'POST':
        likescount = 0
        if request.POST['post_slug'] is not None:
            post_slug = request.POST['post_slug']
            try:
                post = Post.objects.get(slug=post_slug)
            except Post.DoesNotExist:
                context = {'msg':'Like failed', 'status':'error'}
                return HttpResponse(json.dumps(context), status=400);
            try:
                like = Likes.objects.get(post=post, user=request.user)
                likescount = getLikesCount(post.id)
            except Likes.DoesNotExist:
                like = Likes.objects.get_or_create(
                    post=post,
                    user=request.user
                )
                likescount = getLikesCount(post.id)
                context = {'msg':'Like success', 'status':'success', 'likescount':likescount}
                return HttpResponse(json.dumps(context), status=200);
            except Likes.MultipleObjectsReturned:
                like = Likes.objects.get(post=post, user=request.user).delete()
                Likes.objects.get_or_create(
                    post=post,
                    user=request.user
                )
                likescount = getLikesCount(post.id)
                context = {'msg':'Like success', 'status':'success', 'likescount':likescount}
                return HttpResponse(json.dumps(context), status=200);
            like = Likes.objects.filter(post=post, user=request.user).delete()
            likescount = getLikesCount(post.id)
            context = {'msg':'Unike success', 'status':'success', 'likescount':likescount}
            return HttpResponse(json.dumps(context), status=200);
        else:
            context = {'msg':'Invalid post slug', 'status':'error'}
            return HttpResponse(json.dumps(context), status=400);
    else:
        context = {'msg':'Invalid request', 'status':'error'}
        return HttpResponse(json.dumps(context), status=403);

#show all post for selected category
def categoryPost(request, slug):
    try:
        obj_category = Category.objects.get(slug=slug)
        latest_blog_post = Post.objects.filter(category=obj_category).order_by('-created_on')

        # latest_blog_post = Post.objects.order_by('-created_on')[:5]
        category = Category.objects.all()
        context = {'latest_blog_post': latest_blog_post, 'category':category, 'selected_category':obj_category}
    except Category.DoesNotExist:
        raise Http404("Category does not exist")
    return render(request, "home.html", context)

# def handle_uploaded_file(f):
#     with open('some/file/name.txt', 'wb+') as destination:
#         for chunk in f.chunks():
#             destination.write(chunk)

# for posting comment on blog post
@login_required(login_url="/login/")
def saveComment(request):
    if request.method == 'POST':
        if request.POST['post'] is not None or request.POST['comment'] is not None:
            try:
                redirect_url = '/blog/'+request.POST['post']
                post_slug = request.POST['post']
                post = Post.objects.get(slug=post_slug)
                comment = Comment.objects.create(
                    text=request.POST['comment'],
                    post=post,
                    user=request.user
                )
            except Comment.DoesNotExist or Post.DoesNotExist:
                return HttpResponseRedirect(redirect_url)
            return HttpResponseRedirect(redirect_url)
        else:
            return HttpResponseRedirect(redirect_url)
    else:
        return HttpResponseRedirect(redirect_url)


@login_required(login_url="/login/")
def createPost(request):
    category = Category.objects.all()
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
                return render(request, 'create_post.html', {'form': form, 'category':category})
            return HttpResponseRedirect('/user/newpost/success/')
        else:
            return render(request, 'create_post.html', {'form': form, 'category':category})
    else:
        context = {'form':CreatePostForm(), 'category':category}
        return render(request, 'create_post.html', context)

def createPostSuccess(request):
    return HttpResponse("Blog created Successfully!!!")


# method to show blog post details page
def detailPost(request, slug):
    try:
        post = Post.objects.get(slug=slug)
        comment = Comment.objects.filter(post=post.id).order_by('-created_on')[:5]
        category = Category.objects.all()
        likescount = getLikesCount(post.id)
    except Post.DoesNotExist:
        raise Http404("Blog does not exist")
    return render(request, 'detail_post.html', {'blog_post': post,
                'category':category, 'comment':comment, 'likescount':likescount})

# method to register user
@csrf_exempt
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
    return render_to_response('register_success.html')
