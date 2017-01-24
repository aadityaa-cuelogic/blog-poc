from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name="home"),
    url(r'^blog/(?P<slug>[\w-]+)/$', views.detailPost, name='blog_detail'),
    url(r'^user/newpost/$', views.createPost, name='create_post'),
    url(r'^user/newpost/success/$', views.createPostSuccess,
        name='create_post_success'),
    url(r'^user/savecomment$', views.saveComment, name="save_comment"),
    url(r'^category/(?P<slug>[\w-]+)/$', views.categoryPost,
        name='category_post'),
    url(r'^user/newpost/like/$', views.likePost, name="like_post"),
    url(r'^user/(?P<username>[\w-]+)/profile/$', views.userProfile, name='user_profile'),
    url(r'^user/(?P<username>[\w-]+)/updateprofile/$', views.updateProfile, name='update_profile'),
    url(r'^user/dashboard/$', views.userDashboard, name='user_dashboard'),
    url(r'^search/$', views.searchPost, name='search_post'),
]
